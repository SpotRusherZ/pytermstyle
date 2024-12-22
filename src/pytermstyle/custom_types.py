from __future__ import annotations

from typing import Literal, Union, TypedDict

__all__ = [
  'TextStyle', 'Color', 'Colors', 'ColorMode', 'TermOptions'
]

TextStyle = Literal[
  "bold",
  "faint",
  "italic",
  "underline",
  "slow_blink",
  "rapid_blink",
  "conceal",
  "strike",
  "framed",
  "encircled",
  "overlined",
]

Color = Literal[
  "black",
  "red",
  "green",
  "yellow",
  "blue",
  "magenta",
  "cyan",
  "white",
]

ExtendedColor = Literal[
  "dark-red",
  "dark-green",
  "dark-blue",
  "light-red",
  "light-green",
  "light-blue",
  "pink",
  "orange",
  "purple",
  "brown",
  "sky-blue",
  "lime-green",
]

Colors = Union[Color, ExtendedColor]

ColorMode = Literal[
  "foreground",
  "background",
]

Colors4Bit = dict[Color, dict[ColorMode, str]]

# Settings Types


class ColorOptions(TypedDict, total=False):
  rgb: list[str]
  color: str


class TermOptions(TypedDict, total=False):
  style: list[TextStyle]
  foreground: ColorOptions
  background: ColorOptions
