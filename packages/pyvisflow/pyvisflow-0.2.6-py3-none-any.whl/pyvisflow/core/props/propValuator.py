from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyvisflow.core.props.fnsMethodProp import FnsMethodPropInfo
    from pyvisflow.core.props import AbsPropInfo
    from pyvisflow.core.reactive import Reactive
    from pyvisflow.core.props.dataFilterProp import DataFilterPropInfo


class Valuator():
    @abstractmethod
    def cal(self, prop: AbsPropInfo) -> str:
        NotImplementedError()


class LambdaValuator(Valuator):
    def __init__(self) -> None:
        super().__init__()

    def cal(self, prop: AbsPropInfo) -> str:
        return f"()=>{prop.gen_expr()}"


class FnsValuator(Valuator):
    def __init__(self, var: str = 'fns') -> None:
        super().__init__()
        self.var = var

    def cal(self, prop: FnsMethodPropInfo) -> str:
        return f"{self.var}{prop.gen_expr()}"


class DataFilterValuator(Valuator):
    def __init__(self, var: str) -> None:
        super().__init__()
        self.var = var

    def cal(self, prop: DataFilterPropInfo) -> str:
        return f"{prop.gen_expr()}"


class PropValuator(Valuator):
    def __init__(self, reactive: Reactive) -> None:
        super().__init__()
        self.reactive = reactive

    def cal(self, prop: AbsPropInfo):
        return f"getby('{self.reactive._id}',v=> v{prop.gen_expr()})"


class CombineValuator(Valuator):
    def __init__(self) -> None:
        super().__init__()

    def cal(self, prop: AbsPropInfo):
        return prop.gen_expr()


class ConstantsValuator(Valuator):
    def __init__(self) -> None:
        super().__init__()

    def cal(self, prop: AbsPropInfo):
        return prop.gen_expr()
