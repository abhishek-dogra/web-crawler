from pydantic import BaseModel, HttpUrl
from typing import Optional


class URLRequest(BaseModel):
    url: HttpUrl


class OpenGraphMeta(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MetaInfo(BaseModel):
    description: Optional[str] = None
    keywords: Optional[str] = None
    author: Optional[str] = None
    robots: Optional[str] = None
    og: Optional[OpenGraphMeta] = None


class MetadataResponse(BaseModel):
    title: Optional[str] = None
    meta: Optional[MetaInfo] = None
    body: Optional[str] = None
