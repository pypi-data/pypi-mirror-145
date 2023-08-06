from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union

if TYPE_CHECKING:
    from pyvisflow.core.props.propValuator import Valuator


class AbsPropInfo():
    def __init__(self, valuator: Valuator,
                 parent: Union[AbsPropInfo, None]) -> None:
        super().__init__()
        self.valuator = valuator
        self.parent = parent

    @abstractmethod
    def _ex_gen_expr(self) -> str:
        return ''

    def gen_expr(self):
        if self.parent:
            return f'{self.parent.gen_expr()}{self._ex_gen_expr()}'
        return self._ex_gen_expr()
