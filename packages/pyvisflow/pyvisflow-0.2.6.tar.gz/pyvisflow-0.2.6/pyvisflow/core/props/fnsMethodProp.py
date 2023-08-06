from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo
from pyvisflow.core.props.propValuator import FnsValuator

if TYPE_CHECKING:
    from pyvisflow.core.props.typeProp import TypePropInfo


class FnsMethodPropInfo(AbsPropInfo):
    def __init__(self,
                 name: str,
                 args: Optional[List] = None,
                 package_var='fns') -> None:
        super().__init__(FnsValuator(package_var), None)
        self.name = name
        self.args = args or []

    @staticmethod
    def __to_code(v: Union[str, int, TypePropInfo]):
        if (v is None) or isinstance(v, (str, int,List)):
            return value2code(v)
        return v.valuator.cal(v)

    def _ex_gen_expr(self):
        args = ','.join(FnsMethodPropInfo.__to_code(v) for v in self.args)
        return f'.{self.name}({args})'
