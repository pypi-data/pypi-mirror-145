from typing import Any, Dict, Iterable, List, Tuple, Union

from pydantic import BaseModel
from pyvisflow.core.props import SubscriptableTypePropInfo, StrTypePropInfo, NumberTypePropInfo
from pyvisflow.core.props.nameProp import NamePropInfo

from .auto_create._select import _Select


class TSelectOption(BaseModel):
    label: str
    value: int


class Select(_Select):
    def __init__(self, options: Iterable[str], multiple=False) -> None:
        super().__init__()
        options = list(options)

        self._options = options

        self.multiple = multiple

    @property
    def options(self):
        '''
        '''

        p = self.get_prop('options')
        return SubscriptableTypePropInfo[str,StrTypePropInfo](p)

    @options.setter
    def options(self, value: Union[SubscriptableTypePropInfo[str,StrTypePropInfo], bool]):
        '''
        '''
        self.set_prop('options', value)

    @property
    def currentLabels(self):
        p = self.get_prop('currentLabels')
        return SubscriptableTypePropInfo[int, StrTypePropInfo](p)

    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()
        data.update({'options': self._options, 'currentLabels': []})
        return data
