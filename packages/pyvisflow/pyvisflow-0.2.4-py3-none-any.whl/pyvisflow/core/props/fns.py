from __future__ import annotations
from typing import Dict, Optional, TypeVar, Union, TYPE_CHECKING
from pyvisflow.core.props import BoolTypePropInfo
from pyvisflow.core.props.fnsMethodProp import FnsMethodPropInfo
from pyvisflow.core.props.typeProp import NumberTypePropInfo, StrTypePropInfo, TypePropInfo
from pyvisflow.core.props.valueProp import DictValuePropInfo, ValuePropInfo

TIfelse = TypeVar('TIfelse', str, int, Dict)
TMapReturn = TypeVar('TMapReturn', str, int, TypePropInfo)

if TYPE_CHECKING:
    from pyvisflow.app import App


class Fns():
    def __init__(self, app: Optional[App] = None) -> None:
        self.__app = app

    def ifelse(self, condition: BoolTypePropInfo,
               value_if_true: Optional[TIfelse],
               value_if_false: Optional[TIfelse]):

        value_true = ValuePropInfo.try2PropInfo(value_if_true)
        value_false = ValuePropInfo.try2PropInfo(value_if_false)

        m = FnsMethodPropInfo('ifelse', [condition, value_true, value_false])
        if isinstance(value_if_true, str):
            return StrTypePropInfo(m)

        return NumberTypePropInfo(m)

    def map(self,
            key: StrTypePropInfo,
            data: Dict[str, TMapReturn],
            __default=None) -> StrTypePropInfo:
        assert len(data) > 0, 'dict data len must be greater than 0'

        data_value = DictValuePropInfo(None, data)
        m = FnsMethodPropInfo('map', [key, data_value, __default])

        first = list(data.values())[0]
        if isinstance(first, (str, StrTypePropInfo)):
            return StrTypePropInfo(m)

        return NumberTypePropInfo(m)