import aiohttp
from bs4 import BeautifulSoup


async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def extract_metadata(html: str) -> dict:
    soup = BeautifulSoup(html, 'lxml')

    def get_meta(name: str) -> str | None:
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content") if tag else None

    def get_og(property_name: str) -> str | None:
        tag = soup.find("meta", attrs={"property": property_name})
        return tag.get("content") if tag else None

    title = soup.title.string if soup.title else None

    for tag in soup(["script", "style"]):
        tag.decompose()
    body_text = ' '.join(soup.stripped_strings)

    return {
        "title": title,
        "meta": {
            "description": get_meta("description"),
            "keywords": get_meta("keywords"),
            "author": get_meta("author"),
            "robots": get_meta("robots"),
            "og": {
                "title": get_og("title"),
                "description": get_og("description"),
            }
        },
        "body": body_text[:5000],
    }
