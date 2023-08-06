from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, List, Optional, TypeVar, Union, Tuple, Dict, TYPE_CHECKING, Generator
from pyvisflow.core.props.indexProp import IndexPropInfo

from .absProp import AbsPropInfo

if TYPE_CHECKING:
    from pyvisflow.core.props.propValuator import Valuator


class NamePropInfo(AbsPropInfo):
    def __init__(self, valuator: Valuator, parent: Union[AbsPropInfo, None],
                 name: str) -> None:
        super().__init__(valuator, parent)
        self.name = name

    def _ex_gen_expr(self):
        return f'.{self.name}'
