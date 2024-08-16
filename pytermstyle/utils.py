from typing import Optional

from .custom_types import ColorMode, Color
from .definitions import baseColors, extendedColors

def is_rgb_valid(rgb: list[str]) -> bool:
    return all(0 <= int(color) <= 255 for color in rgb)

def get_4bit_color_code(color: Color, mode: ColorMode) -> str:
  code = baseColors.index(color) + (30 if mode == "foreground" else 40)

  return str(code)

def get_8bit_color_code(name: str) -> Optional[str]:
  if name not in extendedColors:
    return name if name.isdigit() and is_rgb_valid([name]) else None

  return extendedColors[name]
