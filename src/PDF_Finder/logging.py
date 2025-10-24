

import asyncio, json, logging, logging.handlers, pathlib, re, urllib.parse, argparse, shutil
from typing import Dict, Any, List, Optional

import httpx
import pandas as pd
import yaml
from pypdf import PdfReader
from tqdm.asyncio import tqdm_asyncio

def setup_logging(cfg: Dict[str, Any], out_dir: pathlib.Path):
    log_cfg = cfg.get("logging", {})
    level = getattr(logging, log_cfg.get("level", "INFO").upper(), logging.INFO)
    (out_dir / "logs").mkdir(parents=True, exist_ok=True)
    log_file = (out_dir / "logs" / log_cfg.get("file", "harvest.log")).resolve()
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=int(log_cfg.get("rotate_bytes", 10_485_760)),
        backupCount=int(log_cfg.get("backup_count", 5)), encoding="utf-8"
    )
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logging.basicConfig(level=level, format=fmt, handlers=[handler, logging.StreamHandler()])
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logging.getLogger("harvest")

