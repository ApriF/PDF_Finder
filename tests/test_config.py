# tests/test_config.py
from pathlib import Path
import yaml
import PDF_Finder as pf

def test_config_defaults():
    cfg = pf.Config(input_excel="input.xlsx")
    assert cfg.input_excel == "input.xlsx"
    assert cfg.doi_column == "doi"
    assert cfg.email == ""
    assert cfg.batch_size == 5
    assert cfg.concurrency == 5
    assert cfg.write_after_each_batch == True
    assert cfg.output_dir == "output"
    
    assert cfg.folders.downloads == "downloads"
    assert cfg.folders.found == "output_found"
    assert cfg.folders.notfound == "output_notfound"

    assert cfg.cache.enabled is True
    assert cfg.cache.force_refresh is False

    assert cfg.http.user_agent == "pdfharvest/1.0"
    assert cfg.http.max_keepalive == 20
    assert cfg.http.max_connections == 20

    assert cfg.timeouts.connect == 15.0
    assert cfg.timeouts.read == 30.0

    assert cfg.logging.level == "INFO"
    assert cfg.logging.file == "harvest.log"
    assert cfg.logging.rotate_bytes == 10_485_760
    assert cfg.logging.backup_count == 5

def test_config_from_yaml(tmp_path: Path):
    yaml_content = {
        "input_excel": "dois.xlsx",
        "doi_column": "doi1",
        "email": "test@student.agh.edu.pl",
        "batch_size": 10,
        "concurrency": 15,
        "write_after_each_batch": False,
        "output_dir": "Output",
        "folders": {"downloads": "dl", "found": "of", "notfound": "onf"},
        "cache": {"enabled": False, "force_refresh": True},
        "http": {"user_agent": "some_agent/1.0", "max_connections": 10, "max_keepalive": 11},
        "timeouts": {"read": 50.5, "connect": 15.5},
        "logging": {"level": "inf", "file": "some_file", "rotate_bytes": 29, "backup_count": 11}
    }

    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text(yaml.safe_dump(yaml_content))

    cfg = pf.Config.from_yaml(yaml_file)
    assert cfg.input_excel == "dois.xlsx"
    assert cfg.doi_column == "doi1"
    assert cfg.email == "test@student.agh.edu.pl"
    assert cfg.batch_size == 10
    assert cfg.concurrency == 15
    assert cfg.write_after_each_batch == False
    assert cfg.output_dir == "Output"
 
    assert cfg.folders.downloads == "dl"
    assert cfg.folders.found == "of"
    assert cfg.folders.notfound == "onf"
    
    assert cfg.cache.enabled is False
    assert cfg.cache.force_refresh is True
    
    assert cfg.http.user_agent == "some_agent/1.0"
    assert cfg.http.max_keepalive == 11
    assert cfg.http.max_connections == 10

    assert cfg.timeouts.connect == 15.5
    assert cfg.timeouts.read == 50.5

    assert cfg.logging.level == "inf"
    assert cfg.logging.file == "some_file"
    assert cfg.logging.rotate_bytes == 29
    assert cfg.logging.backup_count == 11
