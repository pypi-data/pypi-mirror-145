from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union
from pyvisflow.core.props.methodProp import LambdaMethodPropInfo

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo

from pyvisflow.core.props.propValuator import ConstantsValuator, LambdaValuator
import json


class ValuePropInfo(AbsPropInfo):
    def __init__(self, parent: Union[AbsPropInfo, None],
                 value: Union[float, int, str]) -> None:
        super().__init__(ConstantsValuator(), parent)
        self.value = value

    @staticmethod
    def try2PropInfo(value: Any):
        if (value is None) or isinstance(value, (float, str, int)):
            return ValuePropInfo(None, value)

        if isinstance(value, Dict):
            return JsObjectValuePropInfo(None, value)
        return value

    def _ex_gen_expr(self):
        return value2code(self.value)


class _DictEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, AbsPropInfo):
            m = LambdaMethodPropInfo(o)
            return m.valuator.cal(m)
        return super().default(o)


class DictValuePropInfo(AbsPropInfo):
    def __init__(self, parent: Union[AbsPropInfo, None], value: Dict) -> None:
        super().__init__(ConstantsValuator(), parent)
        self.value = value

    @staticmethod
    def try2PropInfo(value: Any):
        if isinstance(value, (dict)):
            return DictValuePropInfo(None, value)
        return value

    def _ex_gen_expr(self):
        def to_code(key, value):
            if not isinstance(value, (AbsPropInfo)):
                value = value2code(value)
            else:
                m = LambdaMethodPropInfo(value)
                value = m.valuator.cal(m)
            return f'[{value2code(key)},{value}]'

        pairs = [to_code(key, value) for key, value in self.value.items()]
        return f"[{','.join(pairs)}]"


class JsObjectValuePropInfo(AbsPropInfo):
    def __init__(self, parent: Union[AbsPropInfo, None], obj: Dict) -> None:
        super().__init__(ConstantsValuator(), parent)
        self.obj = obj

    @staticmethod
    def try2PropInfo(value: Any):
        if isinstance(value, (dict)):
            return DictValuePropInfo(None, value)
        return value

    def _ex_gen_expr(self):
        def to_code(key, value):
            if not isinstance(value, (AbsPropInfo)):
                value = value2code(value)
            else:
                m = LambdaMethodPropInfo(value)
                value = m.valuator.cal(m)
            return f'{value2code(key)}:{value}'

        pairs = [to_code(key, value) for key, value in self.obj.items()]
        return f"{{{','.join(pairs)}}}"
