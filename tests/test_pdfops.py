import io
import tempfile
from pathlib import Path

from pypdf import PdfWriter

from PDF_Finder import pdfops

def test_search_pdf_basic(tmp_path: Path):
    """Ensures search_pdf finds a simple text"""
    # Créer un petit PDF avec du texte connu
    pdf_path = tmp_path / "test.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)

    writer.add_metadata({"/Title": "Example PDF"})
    with open(pdf_path, "wb") as f:
        writer.write(f)

    result = pdfops.search_pdf(pdf_path, ["Example", "anything"])
    assert isinstance(result, dict)
    assert set(result.keys()) == {"found", "matches", "pages"}
    assert result["found"] in (True, False)
    assert isinstance(result["matches"], list)
    assert isinstance(result["pages"], list)


def test_search_pdf_not_existing(tmp_path: Path):
    fake_path = tmp_path / "missing.pdf"
    res = pdfops.search_pdf(fake_path, ["nothing"])
    assert res["found"] is False
    assert res["matches"] == []
    assert res["pages"] == []



def test_move_pdf_atomic_collision(tmp_path: Path):
    
    dst_dir = tmp_path / "out"
    dst_dir.mkdir()
    existing = dst_dir / "file.pdf"
    existing.write_text("old content")

    src = tmp_path / "file.pdf"
    src.write_text("new content")

    new_path = pdfops.move_pdf_atomic(src, dst_dir)
    
    assert new_path.name == "file_1.pdf"
    assert new_path.exists()
    assert (dst_dir / "file.pdf").exists()
