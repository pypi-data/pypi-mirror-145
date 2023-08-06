from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo

from pyvisflow.core.props.propValuator import DataFilterValuator


class DataFilterPropInfo(AbsPropInfo):
    def __init__(self, var: str) -> None:
        super().__init__(DataFilterValuator(var), None)
        self.var = var

    def _ex_gen_expr(self):
        return self.var
