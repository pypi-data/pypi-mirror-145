from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, TypeVar, Union

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo

if TYPE_CHECKING:
    from pyvisflow.core.props.propValuator import Valuator
    from pyvisflow.core.props.typeProp import NumberTypePropInfo, StrTypePropInfo


class IndexPropInfo(AbsPropInfo):
    def __init__(self, valuator: Valuator, parent: Union[AbsPropInfo, None],
                 idx: Union[int, str, StrTypePropInfo, NumberTypePropInfo]
                 ) -> None:
        super().__init__(valuator, parent)
        self.idx = idx

    @staticmethod
    def __to_code(v: Union[str, int, StrTypePropInfo, NumberTypePropInfo]):
        if isinstance(v, (str, int)):
            return value2code(v)
        return v.valuator.cal(v)

    def _ex_gen_expr(self):
        idx = IndexPropInfo.__to_code(self.idx)
        return f'[{idx}]'
