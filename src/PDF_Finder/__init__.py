"""
Usage:
    import PDF_Finder
    from PDF_Finder import Config, run
"""

from __future__ import annotations

__version__ = "1.0.0"

from .config import Config
from .http import backoff_request, fetch_crossref, fetch_unpaywall, best_pdf_url, download_pdf
from .pdfops import search_pdf, move_pdf_atomic
from .orchestrator import run, process_batch_pdfs, prepare_one
from .cache import sanitize_filename
from .logging import setup_logging

__all__ = [
    "Config",
    "backoff_request",
    "fetch_crossref",
    "fetch_unpaywall",
    "best_pdf_url",
    "download_pdf",
    "search_pdf",
    "move_pdf_atomic",
    "run",
    "process_batch_pdfs",
    "prepare_one",
    "sanitize_filename",
    "setup_logging",
]