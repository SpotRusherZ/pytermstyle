from __future__ import annotations

from .custom_types import TextStyle, Color, Colors

base = "\033["
reset = "\033[0m"

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

extendedColors.update({ color: str(index) for index, color in enumerate(baseColors) })
