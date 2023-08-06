from typing import Callable, Dict, Hashable, List, Optional, Set, Tuple, Union
from pydantic import BaseModel, PrivateAttr, Field
from enum import Enum


class TTargetWatchInfo(BaseModel):
    id: str
    path: str
    logic: str


class TLogic(BaseModel):
    logic: str


class TChartFilterTarget(BaseModel):
    id: str
    logic: str


class TTableFilterTarget(BaseModel):
    id: str
    logic: str


class TValueWatch(BaseModel):
    target: TTargetWatchInfo


class TChartFilterWatch(BaseModel):
    target: TChartFilterTarget


class TTableFilterWatch(BaseModel):
    target: TTableFilterTarget


class TWatchInfo(BaseModel):
    values: List[TValueWatch] = []
    chartFilters: List[TChartFilterWatch] = []
    tableFilters: List[TTableFilterWatch] = []
