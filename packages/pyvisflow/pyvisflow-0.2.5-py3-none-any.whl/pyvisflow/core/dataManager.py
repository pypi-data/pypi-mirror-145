from typing import Dict, List, TYPE_CHECKING
import pandas as pd
from pydantic import BaseModel

from pyvisflow.utils.helper import df2array_dict
from pyvisflow.models.TStaticData import TDataframe, TInfo, TColumnsType
from pyvisflow.core.components.file import FileData
# if TYPE_CHECKING:
#     from pyvisflow.core.components.file import FileData
    

def _2infos(df: pd.DataFrame) -> TInfo:
    cols = df.columns.tolist()
    rows = len(df)
    return TInfo(columns=cols, rows=rows)


def _2columnsType(df: pd.DataFrame) -> List[TColumnsType]:
    return [
        TColumnsType(name=name, type=str(t))
        for name, t in zip(df.columns, df.dtypes)
    ]


class TDataFrameInfo(BaseModel):
    id: str
    type: str 


class DataFrameManager():
    def __init__(self) -> None:
        self.df_dict: Dict[str, pd.DataFrame] = {}
        self.fileData_dict: Dict[str, FileData] = {}

    def mark_dataframe(self, data: pd.DataFrame):
        data_id = str(id(data))
        if not data_id in self.df_dict:
            self.df_dict[data_id] = data

        return TDataFrameInfo(id=data_id,type='dataframe')

    def mark_fileData(self, data:FileData):
        data_id = str(id(data))
        if not data_id in self.fileData_dict:
            self.fileData_dict[data_id] = data

        return TDataFrameInfo(id=data._id,type='from-file')

    def reset(self):
        self.df_dict.clear()

    def to_model(self) -> List[TDataframe]:

        return [
            TDataframe(id=id,
                       infos=_2infos(df),
                       columnsType=_2columnsType(df),
                       data=df2array_dict(df))
            for id, df in self.df_dict.items()
        ]
