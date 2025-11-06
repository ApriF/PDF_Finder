# config.py
from __future__ import annotations

import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


@dataclass
class FolderConfig:
    downloads: str = "downloads"
    found: str = "output_found"
    notfound: str = "output_notfound"


@dataclass
class CacheConfig:
    enabled: bool = True
    force_refresh: bool = False


@dataclass
class HttpConfig:
    user_agent: str = "pdfharvest/1.0"
    max_keepalive: int = 20
    max_connections: int = 20


@dataclass
class TimeoutConfig:
    read: float = 30.0
    connect: float = 15.0


@dataclass
class LoggingConfig:
    level: str = "INFO"
    file: str = "harvest.log"
    rotate_bytes: int = 10_485_760
    backup_count: int = 5


@dataclass
class Config:
    input_excel: str
    doi_column: str = "doi"
    email: str = ""
    batch_size: int = 5
    concurrency: int = 5
    write_after_each_batch: bool = True
    strings: list[str] = field(default_factory=list)
    output_dir: str = "output"

    folders: FolderConfig = field(default_factory=FolderConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    http: HttpConfig = field(default_factory=HttpConfig)
    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @staticmethod
    def from_yaml(path: str | Path) -> "Config":
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        def subcls(cls, section):
            return cls(**raw.get(section, {})) if section in raw else cls()

        return Config(
            input_excel=raw.get("input_excel"),
            doi_column=raw.get("doi_column", "doi"),
            email=raw.get("email", ""),
            batch_size=raw.get("batch_size", 5),
            concurrency=raw.get("concurrency", 5),
            write_after_each_batch=raw.get("write_after_each_batch", True),
            strings=raw.get("strings", []),
            output_dir=raw.get("output_dir", "output"),
            folders=subcls(FolderConfig, "folders"),
            cache=subcls(CacheConfig, "cache"),
            http=subcls(HttpConfig, "http"),
            timeouts=subcls(TimeoutConfig, "timeouts"),
            logging=subcls(LoggingConfig, "logging"),
        )


