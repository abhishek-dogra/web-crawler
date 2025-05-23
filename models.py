from pydantic import BaseModel, HttpUrl


class URLRequest(BaseModel):
    url: HttpUrl


class MetadataResponse(BaseModel):
    title: str | None
    description: str | None
    keywords: str | None
    body_text: str | None
