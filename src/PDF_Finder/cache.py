




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

