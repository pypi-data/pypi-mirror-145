from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="CanvasUiBlock")


@attr.s(auto_attribs=True, repr=False)
class CanvasUiBlock:
    """  """

    def __repr__(self):
        fields = []
        return "CanvasUiBlock({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        canvas_ui_block = cls()

        return canvas_ui_block
