


import asyncio, json, logging, logging.handlers, pathlib, re, urllib.parse, argparse, shutil
from typing import Dict, Any, List, Optional

import httpx
import pandas as pd
import yaml
from pypdf import PdfReader
from tqdm.asyncio import tqdm_asyncio

# CLI shim
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Batched DOI harvester: staged downloads → processing → routed outputs")
    ap.add_argument("--config", required=True, help="Path to YAML config")
    args = ap.parse_args()
    asyncio.run(run(args.config))
