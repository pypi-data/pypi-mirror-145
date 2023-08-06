from pyvisflow.core.components.components import Component
from pyvisflow.core.props import TypePropInfo
from pyvisflow.models.TComponent import TComponentType


class MarkdownValue(Component):
    def __init__(self) -> None:
        super().__init__('markdown-value', TComponentType.builtIn)

    def set_value(self, prop: TypePropInfo):
        self.set_prop('value', prop)
