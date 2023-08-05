from collections.abc import Sequence
from typing import Any, overload

from typing_extensions import Literal

from .matrix import Matrix

_Glyph = tuple[int, float, float]

class FontFace:
    def __init__(self, pointer: Any) -> None: ...

class ToyFontFace(FontFace):
    def __init__(
        self, family: str = ..., slant: int = ..., weight: int = ...
    ) -> None: ...
    def get_family(self) -> str: ...
    def get_slant(self) -> int: ...
    def get_weight(self) -> int: ...

class ScaledFont:
    def __init__(
        self,
        font_face: FontFace,
        font_matrix: Matrix | None = ...,
        ctm: Matrix | None = ...,
        options: FontOptions | None = ...,
    ) -> None: ...
    def get_font_face(self) -> FontFace: ...
    def get_font_options(self) -> FontOptions: ...
    def get_font_matrix(self) -> Matrix: ...
    def get_ctm(self) -> Matrix: ...
    def get_scale_matrix(self) -> Matrix: ...
    def extents(self) -> tuple[float, float, float, float, float]: ...
    def text_extents(
        self, text: str
    ) -> tuple[float, float, float, float, float, float]: ...
    def glyph_extents(
        self, glyphs: Sequence[_Glyph]
    ) -> tuple[float, float, float, float, float, float]: ...
    @overload
    def text_to_glyphs(
        self, x: float, y: float, text: str, with_clusters: Literal[True]
    ) -> tuple[list[_Glyph], list[tuple[int, int]], int]: ...
    @overload
    def text_to_glyphs(
        self, x: float, y: float, text: str, with_clusters: Literal[False]
    ) -> list[_Glyph]: ...

class FontOptions:
    def __init__(self, **values: int) -> None: ...
    def copy(self) -> FontOptions: ...
    def merge(self, other: FontOptions) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: FontOptions) -> bool: ...
    def __ne__(self, other: FontOptions) -> bool: ...
    def equal(self, other: FontOptions) -> bool: ...
    def hash(self) -> int: ...
    def set_antialias(self, antialias: int) -> None: ...
    def get_antialias(self) -> int: ...
    def set_subpixel_order(self, subpixel_order: int) -> None: ...
    def get_subpixel_order(self) -> int: ...
    def set_hint_style(self, hint_style: int) -> None: ...
    def get_hint_style(self) -> int: ...
    def set_hint_metrics(self, hint_metrics: int) -> None: ...
    def get_hint_metrics(self) -> int: ...
    def set_variations(self, variations: int) -> None: ...
    def get_variations(self) -> int: ...
