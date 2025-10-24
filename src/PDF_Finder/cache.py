

# ---------------- Utils & dirs ----------------

def sanitize_filename(s: str) -> str:
    s = s.strip().replace("doi:", "").replace("DOI:", "")
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)

def ensure_dirs(base: pathlib.Path, cfg: Dict[str, Any]):
    (base / "cache" / "crossref").mkdir(parents=True, exist_ok=True)
    (base / "cache" / "unpaywall").mkdir(parents=True, exist_ok=True)
    (base / "cache" / "matches").mkdir(parents=True, exist_ok=True)
    # staging + final folders
    (base / cfg["folders"]["downloads"]).mkdir(parents=True, exist_ok=True)
    (base / cfg["folders"]["found"]).mkdir(parents=True, exist_ok=True)
    (base / cfg["folders"]["notfound"]).mkdir(parents=True, exist_ok=True)

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}



def cache_path(base: pathlib.Path, ns: str, doi: str) -> pathlib.Path:
    return base / "cache" / ns / f"{sanitize_filename(doi)}.json"

def read_cache_json(path: pathlib.Path) -> Optional[Dict[str, Any]]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def write_cache_json(path: pathlib.Path, data: Dict[str, Any]):
    try:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        logging.getLogger("harvest").warning(f"Cache write failed {path}: {e}")

