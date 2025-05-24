import aiohttp
from bs4 import BeautifulSoup
from typing import Optional


async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def get_meta(soup: BeautifulSoup, name: str) -> Optional[str]:
    tag = soup.find("meta", attrs={"name": name})
    return tag.get("content") if tag and tag.has_attr("content") else None


def get_og(soup: BeautifulSoup, property_name: str) -> Optional[str]:
    tag = soup.find("meta", attrs={"property": property_name})
    return tag.get("content") if tag and tag.has_attr("content") else None


def extract_meta_tags(soup: BeautifulSoup) -> Optional[dict]:
    meta_tags = {
        "description": get_meta(soup, "description"),
        "keywords": get_meta(soup, "keywords"),
        "author": get_meta(soup, "author"),
        "robots": get_meta(soup, "robots"),
    }
    og_tags = {
        "title": get_og(soup, "og:title"),
        "description": get_og(soup, "og:description"),
    }

    meta_tags = {k: v for k, v in meta_tags.items() if v}
    og_tags = {k: v for k, v in og_tags.items() if v}

    if og_tags:
        meta_tags["og"] = og_tags

    return meta_tags if meta_tags else None


def extract_body_text(soup: BeautifulSoup) -> Optional[str]:
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)
    return text[:5000] if text else None


def extract_metadata(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    metadata = {}

    title = soup.title.string.strip() if soup.title and soup.title.string else None
    if title:
        metadata["title"] = title

    meta = extract_meta_tags(soup)
    if meta:
        metadata["meta"] = meta

    body = extract_body_text(soup)
    if body:
        metadata["body"] = body

    return metadata
