from typing import Dict, List, Optional, Union
from pyvisflow.core.components.components import Component
from pyvisflow.core.dataManager import DataFrameManager, TDataFrameInfo
from pyvisflow.core.props import StrTypePropInfo, SubscriptableTypePropInfo, BoolTypePropInfo
from pyvisflow.core.props.dataFilterProp import DataFilterPropInfo
from pyvisflow.core.props.nameProp import NamePropInfo
from pyvisflow.models.TWatchInfo import TTableFilterWatch, TTableFilterTarget
from pyvisflow.utils.helper import df2object_dict
from .auto_create._dataTable import _DataTable
import pandas as pd


class DataTable(_DataTable):
    def __init__(self, data_info: TDataFrameInfo) -> None:
        super().__init__()

        self._data_id = data_info
        self.current_page = 1
        self._filter_watch_infos: List[TTableFilterWatch] = []

    def __getitem__(self, column: Union[str, StrTypePropInfo]):
        p = DataFilterPropInfo('row')
        subs = SubscriptableTypePropInfo[str, StrTypePropInfo](p)

        return subs[column]

    def query(self, condition: BoolTypePropInfo):
        logic = condition.valuator.cal(condition)
        target = TTableFilterTarget(id=self._id, logic=logic)
        filter = TTableFilterWatch(target=target)
        self._filter_watch_infos.append(filter)

    @property
    def rowClick(self):
        p = self.get_prop('rowClick')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)

    @property
    def rowHover(self):
        p = self.get_prop('rowHover')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)

    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()
        data.update({
            'dataInfo': self._data_id,
            'rowClick': {},
            'rowHover': {},
        })
        return data
