
# http_utils.py
from __future__ import annotations

import asyncio
import logging
import urllib.parse
from typing import Any, Dict, Optional
import pathlib

import httpx

CROSSREF = "https://api.crossref.org/works/"
UNPAYWALL = "https://api.unpaywall.org/v2/"

async def backoff_request(client: httpx.AsyncClient, method: str, url: str, **kwargs) -> httpx.Response:
    log = logging.getLogger("harvest")
    max_tries, base = 6, 0.5
    for i in range(max_tries):
        try:
            r = await client.request(method, url, **kwargs)
            if r.status_code in (429, 500, 502, 503, 504):
                ra = r.headers.get("Retry-After")
                wait = float(ra) if ra else min(base * (2**i), 10.0)
                log.warning(f"{r.status_code} {url} → backoff {wait:.2f}s (try {i+1}/{max_tries})")
                await asyncio.sleep(wait); continue
            r.raise_for_status()
            return r
        except httpx.HTTPError as e:
            if i == max_tries - 1:
                log.error(f"HTTP error {url}: {e}")
                raise
            await asyncio.sleep(min(base * (2**i), 10.0))
    raise RuntimeError("unreachable")

async def fetch_crossref(client: httpx.AsyncClient, doi: str) -> Dict[str, Any]:
    r = await backoff_request(client, "GET", CROSSREF + urllib.parse.quote(doi), timeout=20)
    return r.json().get("message", {})

async def fetch_unpaywall(client: httpx.AsyncClient, doi: str, email: str) -> Dict[str, Any]:
    r = await backoff_request(client, "GET", UNPAYWALL + urllib.parse.quote(doi),
                              params={"email": email}, timeout=20)
    if r.status_code == 404:
        return {}
    return r.json()

def best_pdf_url(ua: Dict[str, Any]) -> Optional[str]:
    if not ua: return None
    loc = ua.get("best_oa_location") or {}
    pdf = loc.get("url_for_pdf") or loc.get("url")
    if pdf: return pdf
    for loc in ua.get("oa_locations") or []:
        pdf = loc.get("url_for_pdf") or loc.get("url")
        if pdf: return pdf
    return None



async def download_pdf(client: httpx.AsyncClient, url: str, out_path: pathlib.Path) -> bool:
    log = logging.getLogger("harvest")
    try:
        async with client.stream("GET", url, timeout=40) as r:
            if r.status_code >= 400:
                log.warning(f"PDF {url} → {r.status_code}")
                return False
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f:
                async for chunk in r.aiter_bytes():
                    f.write(chunk)
        with open(out_path, "rb") as f:
            if f.read(4) != b"%PDF":
                log.warning(f"Not a PDF (magic header) → {url}")
                out_path.unlink(missing_ok=True); return False
        return True
    except Exception as e:
        log.warning(f"PDF download failed {url}: {e}")
        return False
