from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from enum import Enum


class TInfo(BaseModel):
    columns: List[str]
    rows: int


class TColumnsType(BaseModel):
    name: str
    type: str


class TDataframe(BaseModel):
    id: str
    infos: TInfo
    columnsType: List[TColumnsType]
    data: List[List[Any]]


class TStaticData(BaseModel):
    dataframes: List[TDataframe]
