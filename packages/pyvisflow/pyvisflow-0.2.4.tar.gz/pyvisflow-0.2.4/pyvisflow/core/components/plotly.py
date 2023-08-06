from typing import Dict, List, Optional
from pyvisflow.core.props import StrTypePropInfo, SubscriptableTypePropInfo
from pyvisflow.core.props.dataFilterProp import DataFilterPropInfo
from pyvisflow.core.props.nameProp import NamePropInfo
from pyvisflow.core.props.typeProp import BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.dataManager import TDataFrameInfo
from pyvisflow.models.TWatchInfo import TChartFilterTarget, TChartFilterWatch
from .components import Component


class Plotly(Component):
    def __init__(self,data_info: Optional[TDataFrameInfo]=None,) -> None:
        super().__init__('plotly', TComponentType.builtIn)
        self._data_info = data_info
        self._data: List[Dict] = []
        self._layout = {}
        self._filter_watch_infos: List[TChartFilterWatch] = []
        self.__dataPropsReplace:List[Dict]=[]

    @property
    def clickInfo(self):
        p = self.get_prop('clickInfo')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)

    @property
    def hoverInfo(self):
        p = self.get_prop('hoverInfo')
        # sub = SubscriptableTypePropInfo[str, SubscriptableTypePropInfo](p)
        return HoverInfoPropInfo(p)

    def from_dict(self, data:Dict):
        if 'data' in data:
            for d in data['data']:
                self.add_data(d)

        if 'layout' in data:
            self.update_layout(data['layout'])
        return self

    def from_fig(self, fig):
        return self.from_dict(fig.to_dict())

    def add_data(self, data: Dict):
        self._data.append(data)
        return self

    def update_data(self, idx: int, data: Dict):
        self._data[idx].update(data)
        return self

    def update_layout(self, layout: Dict):
        self._layout.update(layout)
        return self

    def encode(self,path:str,column:str):
        self.__dataPropsReplace.append({'path':path,'column':column})
        return self

    def filters(self, condition: BoolTypePropInfo):
        logic = condition.valuator.cal(condition)
        target = TChartFilterTarget(id=self._id, logic=logic)
        filter = TChartFilterWatch(target=target)
        self._filter_watch_infos.append(filter)

    @property
    def data(self):
        p = DataFilterPropInfo('row')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)

    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()

        info_id = None
        if self._data_info:
            info_id = self._data_info.id
        data.update({
            'dataInfo': {
                'id': info_id
            },
            'dataPropsReplace':self.__dataPropsReplace,
            'data': self._data,
            'layout': self._layout,
            'config': {},
            'clickInfo': {},
            'hoverInfo': {
                'infos': {
                    'x': None,
                    'y': None
                }
            },
        })

        return data


class HoverInfoPropInfo(SubscriptableTypePropInfo):
    def __init__(self, parent) -> None:
        super().__init__(parent)

    @property
    def x(self):
        n = NamePropInfo(self.valuator, self, 'infos.x')
        return StrTypePropInfo(n)

    @property
    def y(self):
        n = NamePropInfo(self.valuator, self, 'infos.y')
        return StrTypePropInfo(n)