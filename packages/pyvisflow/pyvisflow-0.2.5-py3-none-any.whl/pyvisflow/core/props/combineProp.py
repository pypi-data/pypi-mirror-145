from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator

from .absProp import AbsPropInfo
from pyvisflow.core.props.propValuator import CombineValuator
if TYPE_CHECKING:
    from .propValuator import Valuator


class CombinePropInfo(AbsPropInfo):
    def __init__(self, logic: str, left: AbsPropInfo,
                 right: AbsPropInfo) -> None:
        super().__init__(CombineValuator(), None)
        self.left = left
        self.right = right
        self.logic = logic

    def _ex_gen_expr(self):
        left = self.left.valuator.cal(self.left)
        right = self.right.valuator.cal(self.right)
        return f'({left}{self.logic}{right})'
