from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union
from pyvisflow.core.props.propValuator import FnsValuator

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo

if TYPE_CHECKING:
    from pyvisflow.core.props.propValuator import Valuator


class MethodPropInfo(AbsPropInfo):
    def __init__(self,
                 valuator: Valuator,
                 parent: Union[AbsPropInfo, None],
                 name: str,
                 args: Optional[List] = None) -> None:
        super().__init__(valuator, parent)
        self.name = name
        self.args = args or []

    def _ex_gen_expr(self):
        args = ','.join(value2code(v) for v in self.args)
        return f'?.{self.name}({args})'


class LambdaMethodPropInfo(AbsPropInfo):
    def __init__(self, value: AbsPropInfo,args:Optional[List[str]]=None) -> None:

        var = f"({','.join(args or [])})=>"

        super().__init__(FnsValuator(var), None)
        self.value = value

    def _ex_gen_expr(self):
        return self.value.valuator.cal(self.value)