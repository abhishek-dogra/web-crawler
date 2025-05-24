from fastapi import FastAPI, HTTPException
from crawler import fetch_html, extract_metadata
from models import URLRequest, MetadataResponse
from robots import is_allowed
import logging

app = FastAPI(title="URL Metadata Extractor")

logger = logging.getLogger("uvicorn.error")


@app.head("/")
async def health_check():
    return {"status": "ok", "message": "Service is healthy"}


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Service is healthy"}


@app.post("/extract", response_model=MetadataResponse)
async def extract_url_metadata(request: URLRequest):
    url = str(request.url)
    try:
        if not await is_allowed(url):
            raise HTTPException(status_code=403, detail="Crawling disallowed by robots.txt")
        html = await fetch_html(url)
        metadata = extract_metadata(html)
        return metadata
    except Exception as e:
        logger.exception(f"Error extracting metadata for {url} with exception {e}")
        raise HTTPException(status_code=500, detail="Failed to extract metadata")
