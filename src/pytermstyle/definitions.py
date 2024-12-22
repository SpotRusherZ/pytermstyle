from __future__ import annotations

from .custom_types import TextStyle, Color, Colors

__all__ = [
  'BASE', 'RESET', 'FG_RGB_CODE', 'BG_RGB_CODE', 'FG_COLOR_CODE',
  'BG_COLOR_CODE', 'textStyles', 'baseColors', 'extendedColors'
]

BASE = "\033["
RESET = "\033[0m"
FG_RGB_CODE = ["38", "2"]
BG_RGB_CODE = ["48", "2"]
FG_COLOR_CODE = ["38", "5"]
BG_COLOR_CODE = ["48", "5"]

textStyles: dict[TextStyle, str] = {
  "bold": "1",
  "faint": "2",
  "italic": "3",
  "underline": "4",
  "slow_blink": "5",
  "rapid_blink": "6",
  "conceal": "8",
  "strike": "9",
  "framed": "51",
  "encircled": "52",
  "overlined": "53",
}

baseColors: list[Color] = [
  "black",
  "red",
  "green",
  "yellow",
  "blue",
  "magenta",
  "cyan",
  "white",
]

extendedColors: dict[Colors, str] = {
  "dark-red": "88",
  "dark-green": "22",
  "dark-blue": "18",
  "light-red": "196",
  "light-green": "120",
  "light-blue": "81",
  "pink": "13",
  "orange": "214",
  "purple": "93",
  "brown": "94",
  "sky-blue": "153",
  "lime-green": "156",
}

extendedColors.update({color: str(index) for index, color in enumerate(baseColors)})
