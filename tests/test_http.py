# tests/test_http.py
import pytest
import httpx
import PDF_Finder as pf

from unittest.mock import AsyncMock, patch


# ruff formatting
@pytest.mark.asyncio
async def test_backoff_request_success():
    """Simulate a successful HTTP request."""

    async def handler(request):
        return httpx.Response(200, json={"message": "ok"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        response = await pf.backoff_request(client, "GET", "https://example.com")
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}


@pytest.mark.asyncio
async def test_backoff_request_retries(monkeypatch):
    """Simulate temporary 429 errors before success."""
    calls = {"count": 0}

    async def handler(request):
        calls["count"] += 1
        if calls["count"] < 6:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"done": True})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        response = await pf.backoff_request(client, "GET", "https://example.com")
        assert response.status_code == 200
        assert calls["count"] == 6


@pytest.mark.asyncio
async def test_download_pdf_success(tmp_path):
    file_path = tmp_path / "out.pdf"
    content = b"%PDF-AGH rocks"

    # NOT async here — returns a FakeStream directly
    def fake_stream_request(*args, **kwargs):
        class FakeStream:
            status_code = 200

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                pass

            async def aiter_bytes(self):
                yield content

        return FakeStream()

    client = AsyncMock(spec=httpx.AsyncClient)
    client.stream = fake_stream_request

    result = await pf.download_pdf(client, "https://example.com", file_path)

    assert result is True
    assert file_path.exists()
    assert file_path.read_bytes().startswith(b"%PDF-AGH rocks")


@pytest.mark.asyncio
async def test_download_pdf_invalid_pdf(tmp_path):
    file_path = tmp_path / "bad.pdf"
    content = b"%DOCX yikes"

    def fake_stream_request(*args, **kwargs):
        class FakeStream:
            status_code = 200

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                pass

            async def aiter_bytes(self):
                yield content

        return FakeStream()

    client = AsyncMock(spec=httpx.AsyncClient)
    client.stream = fake_stream_request

    result = await pf.download_pdf(client, "https://example.com", file_path)
    assert result is False
    assert not file_path.exists()


def test_best_pdf_url_best_location():
    ua = {
        "best_oa_location": {"url_for_pdf": "https://example.com/best.pdf"},
        "oa_locations": [{"url": "https://example.com/fallback.pdf"}],
    }
    assert pf.best_pdf_url(ua) == "https://example.com/best.pdf"


def test_best_pdf_url_fallback_locations():
    ua = {
        "best_oa_location": None,
        "oa_locations": [{"url": "https://example.com/fallback.pdf"}],
        "oa_locations": [{"url_for_pdf": "https://example.com/fallback1.pdf"}],
    }
    assert pf.best_pdf_url(ua) == "https://example.com/fallback1.pdf"


def test_best_pdf_url_no_url():
    assert pf.best_pdf_url({}) is None
