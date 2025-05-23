from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

import aiohttp


async def is_allowed(url: str, user_agent: str = "*") -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = RobotFileParser()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(robots_url) as response:
                text = await response.text()
                rp.parse(text.splitlines())
    except Exception:
        return True

    return rp.can_fetch(user_agent, url)
