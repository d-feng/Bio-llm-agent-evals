"""
tools/ncbi_gene_tool.py
-----------------------
LangChain tool for querying the NCBI Gene database via E-utilities.
Returns verified genomic metadata (gene symbol, chromosome, aliases, map location).
"""

import json
import requests
from langchain_core.tools import tool

NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
HEADERS = {"User-Agent": "LangGraph-Genomic-Agent/1.0"}
EMAIL = "agent.architect@biopharma.com"


@tool
def search_ncbi_gene(query: str, max_results: int = 3) -> str:
    """
    Queries the NCBI Gene database to retrieve verified genomic metadata.
    Input:  A search term like 'ERBB2[sym] AND human[orgn]' or 'rs1229984'.
    Output: A JSON-formatted string containing gene summaries, aliases, and map locations.
    """
    try:
        # Step 1: ESearch — get NCBI UIDs matching the query
        search_params = {
            "db": "gene",
            "term": query,
            "retmode": "json",
            "retmax": max_results,
            "email": EMAIL,
        }
        search_res = requests.get(
            f"{NCBI_BASE_URL}/esearch.fcgi", params=search_params, headers=HEADERS
        )
        search_res.raise_for_status()
        id_list = search_res.json().get("esearchresult", {}).get("idlist", [])

        if not id_list:
            return f"No results found in NCBI Gene database for query: {query}"

        # Step 2: ESummary — fetch metadata for the retrieved UIDs
        summary_params = {
            "db": "gene",
            "id": ",".join(id_list),
            "retmode": "json",
            "email": EMAIL,
        }
        summary_res = requests.get(
            f"{NCBI_BASE_URL}/esummary.fcgi", params=summary_params, headers=HEADERS
        )
        summary_res.raise_for_status()

        # Step 3: Extract high-value fields for the LLM context
        summaries = summary_res.json().get("result", {})
        results = []
        for uid in id_list:
            if uid in summaries:
                data = summaries[uid]
                results.append({
                    "UID": uid,
                    "Name": data.get("name"),
                    "Description": data.get("description"),
                    "Chromosome": data.get("chromosome"),
                    "MapLocation": data.get("maplocation"),
                    "Aliases": data.get("otheraliases"),
                })

        return json.dumps(results, indent=2)

    except requests.exceptions.RequestException as e:
        return f"NCBI API Error: {str(e)}"


@tool
def search_ensembl_gene(identifier: str) -> str:
    """
    Queries the Ensembl REST API to look up gene metadata by Ensembl gene ID,
    gene symbol, BAC clone name, or GenBank accession.
    Input:  An Ensembl ID (e.g. 'ENSG00000141510'), gene symbol, or other identifier.
    Output: A JSON-formatted string with gene name, chromosome, start/end position,
            biotype, and description.
    """
    ENSEMBL_BASE = "https://rest.ensembl.org"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Clean up the identifier
    ident = identifier.strip()

    try:
        # Route 1: Ensembl stable ID (ENSG...)
        if ident.upper().startswith("ENSG"):
            url = f"{ENSEMBL_BASE}/lookup/id/{ident}"
            resp = requests.get(url, headers=headers, params={"expand": 0})
            resp.raise_for_status()
            data = resp.json()
            return json.dumps({
                "Identifier": ident,
                "Name": data.get("display_name"),
                "Chromosome": f"chr{data.get('seq_region_name')}",
                "Start": data.get("start"),
                "End": data.get("end"),
                "Strand": data.get("strand"),
                "Biotype": data.get("biotype"),
                "Description": data.get("description"),
            }, indent=2)

        # Route 2: Symbol or alias lookup (human, GRCh38)
        url = f"{ENSEMBL_BASE}/lookup/symbol/homo_sapiens/{ident}"
        resp = requests.get(url, headers=headers, params={"expand": 0})
        if resp.status_code == 200:
            data = resp.json()
            return json.dumps({
                "Identifier": ident,
                "EnsemblID": data.get("id"),
                "Name": data.get("display_name"),
                "Chromosome": f"chr{data.get('seq_region_name')}",
                "Start": data.get("start"),
                "End": data.get("end"),
                "Biotype": data.get("biotype"),
                "Description": data.get("description"),
            }, indent=2)

        # Route 3: Sequence region / accession search via xrefs
        url = f"{ENSEMBL_BASE}/xrefs/symbol/homo_sapiens/{ident}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200 and resp.json():
            hits = resp.json()
            ensembl_id = hits[0].get("id")
            if ensembl_id:
                url2 = f"{ENSEMBL_BASE}/lookup/id/{ensembl_id}"
                resp2 = requests.get(url2, headers=headers, params={"expand": 0})
                resp2.raise_for_status()
                data = resp2.json()
                return json.dumps({
                    "Identifier": ident,
                    "EnsemblID": ensembl_id,
                    "Name": data.get("display_name"),
                    "Chromosome": f"chr{data.get('seq_region_name')}",
                    "Start": data.get("start"),
                    "End": data.get("end"),
                    "Biotype": data.get("biotype"),
                    "Description": data.get("description"),
                }, indent=2)

        return f"No Ensembl record found for identifier: {ident}"

    except requests.exceptions.RequestException as e:
        return f"Ensembl API Error: {str(e)}"


@tool
def search_ncbi_snp(rsid: str) -> str:
    """
    Queries the NCBI dbSNP database to retrieve chromosome location and allele
    information for a given SNP rsID.
    Input:  An rsID like 'rs1229984' or 'rs334'.
    Output: A JSON-formatted string with chromosome, position, alleles, and gene context.
    """
    # Strip 'rs' prefix if provided — dbSNP ESearch expects the numeric ID
    rsid_clean = rsid.lower().replace("rs", "").strip()

    try:
        # Step 1: ESearch — look up the SNP in dbSNP
        search_params = {
            "db": "snp",
            "term": rsid_clean,
            "retmode": "json",
            "retmax": 1,
            "email": EMAIL,
        }
        search_res = requests.get(
            f"{NCBI_BASE_URL}/esearch.fcgi", params=search_params, headers=HEADERS
        )
        search_res.raise_for_status()
        id_list = search_res.json().get("esearchresult", {}).get("idlist", [])

        if not id_list:
            return f"No results found in NCBI dbSNP for rsID: rs{rsid_clean}"

        # Step 2: ESummary — fetch SNP metadata
        summary_params = {
            "db": "snp",
            "id": ",".join(id_list),
            "retmode": "json",
            "email": EMAIL,
        }
        summary_res = requests.get(
            f"{NCBI_BASE_URL}/esummary.fcgi", params=summary_params, headers=HEADERS
        )
        summary_res.raise_for_status()

        # Step 3: Parse chromosome and position from the SNP summary
        result_data = summary_res.json().get("result", {})
        records = []
        for uid in id_list:
            if uid in result_data:
                data = result_data[uid]
                chrom = data.get("chr", "")
                # genes is a list of dicts: [{"name": "ADH1B", "gene_id": "125"}]
                genes = data.get("genes", [])
                gene_names = ", ".join(g.get("name", "") for g in genes) if isinstance(genes, list) else ""
                records.append({
                    "rsID": f"rs{rsid_clean}",
                    "Chromosome": f"Chromosome {chrom}" if chrom else "Unknown",
                    "GenomicAccession": data.get("acc", ""),
                    "SPDI": data.get("spdi", ""),
                    "FunctionalClass": data.get("fxn_class", ""),
                    "GeneContext": gene_names,
                    "ClinicalSignificance": data.get("clinical_significance", ""),
                })

        return json.dumps(records, indent=2)

    except requests.exceptions.RequestException as e:
        return f"NCBI dbSNP API Error: {str(e)}"
