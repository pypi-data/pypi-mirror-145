from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum


class TComponentType(str, Enum):
    htmlRaw = 'html-raw'
    htmlRawString = 'html-raw-string'
    builtIn = 'built-in'


class TComponent(BaseModel):
    id: str
    tag: str
    type: TComponentType
    attrs: Optional[Dict] = {}
    styles: Optional[Dict] = {}
    children: Optional[List['TComponent']] = []
