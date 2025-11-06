import asyncio
import pandas as pd
from pathlib import Path
from PDF_Finder.orchestrator import run

def test_run_creates_output(tmp_path: Path):

    excel_path = tmp_path / "dois.xlsx"
    df = pd.DataFrame({"doi": ["10.1234/fake1", "10.5678/fake2"]})
    df.to_excel(excel_path, index=False)

    # yaml file
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(
        f"""
email: test@example.com
input_excel: {excel_path}
output_dir: {tmp_path / "output"}
batch_size: 1
folders:
  downloads: downloads
  found: found
  notfound: notfound
cache:
  enabled: false
strings: ["example", "test"]
"""
    )

    out_df = asyncio.run(run(str(cfg_path)))

    out_dir = tmp_path / "output"
    assert out_dir.exists(), "Le dossier output doit être créé"
    assert (out_dir / "report.xlsx").exists(), "Le rapport Excel doit exister"
    assert (out_dir / "report.csv").exists(), "Le rapport CSV doit exister"

    saved_df = pd.read_excel(out_dir / "report.xlsx")
    assert isinstance(out_df, pd.DataFrame)
    assert len(saved_df) == len(out_df)

    for sub in ["downloads", "found", "notfound", "cache"]:
        assert (out_dir / sub).exists(), f"Le dossier {sub} doit exister"
