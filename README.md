# PDF_Finder

**PDF Finder** is a two-stage asynchronous tool that retrieves and analyzes academic papers using **Crossref** and **Unpaywall** APIs.  
It automatically finds Open Access versions of research papers (via their DOIs), downloads their PDFs, and scans them for specific keywords or phrases.



## Features

- DOI-based metadata retrieval (Crossref + Unpaywall)
- Asynchronous batch processing for faster downloads
- Automatic PDF download and text search
- Incremental Excel & CSV reporting
- Local caching for faster re-runs
- Organized folder structure for outputs

## Installation

### Repository

bash
git clone https://github.com/ApriF/PDF_Finder.git
cd PDF_Finder

### Structure
PDF_Finder/
├── src/
│ └── PDF_Finder/
│ ├── init.py
│ ├── orchestrator.py
│ ├── config.py
│ ├── cache.py
│ ├── http.py
│ ├── pdfops.py
│ ├── logging.py
│ └── cli.py
├── tests/
├── data/
├── output/
├── pyproject.toml
├── requirements.txt
├── config.yaml
└── README.md


### Environment

python -m venv .venv
.venv\Scripts\Activate.ps1

### Dependencies 

pip install -r requirements.txt

## How It Works
The program operates in two stages for each batch of DOIs:

### Stage 1 — Metadata Fetch & PDF Download

Queries Crossref and Unpaywall for metadata
Retrieves Open Access PDF URLs
Downloads PDFs into output/downloads/

### Stage 2 — PDF Processing & Classification
Scans each PDF for the strings defined in the config
Moves each file into output/found/ or output/notfound/
Updates the final report with search results
Reports are generated incrementally in output/report.xlsx and output/report.csv.

### Running the program
Prepare the config.yaml with e-mail and doi

### Excel file
Your Excel file (e.g. data/doi_list.xlsx) should contain at least one column named doi:

example: 
doi
10.1038/s41586-020-2649-2
10.1103/PhysRevLett.127.123456

### Run 

pdf-finder --config config.yaml

### Output structure: 
output/
├── cache/
├── downloads/
├── found/
├── notfound/
├── report.xlsx
└── report.csv

### Test 
pytest -v