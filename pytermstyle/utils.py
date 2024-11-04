from __future__ import annotations

from typing import Optional, get_args

from .custom_types import ColorMode, Color
from .definitions import baseColors, extendedColors

__all__ = [
  'is_rgb_valid', 'is_valid_color', 'get_4bit_color_code', 'get_8bit_color_code'
]

def is_rgb_valid(rgb: list[str]) -> bool:
  """
  Returns True if all values are valid RGB code
  """
  try:
    return all(0 <= int(color) <= 255 for color in rgb)
  except ValueError:
    return False

def is_valid_color(name: str) -> bool:
  """
  Returns True if `name` is a supported color name\n
  (See `Colors` type) or a valid custom color code
  """
  if name not in extendedColors:
    return name.isdigit() and is_rgb_valid([name])

  return True

def get_4bit_color_code(color: Color, mode: ColorMode) -> str:
  """
  Returns the 4-bit code for basic colors.

  Supported by variety of terminal emulators
  """
  if color not in baseColors:
    raise ValueError(f"Color {color} does not have a supported 4-bit code")

  check_invalid_mode(mode)

  code = baseColors.index(color) + (30 if mode == "foreground" else 40)

  return str(code)

def get_8bit_color_code(name: str) -> Optional[str]:
  """
  Returns the code for 8-bit (256) predefined colors.\n
  Some colors can be passed by name (See `Colors` type)\n
  For the remaining colors, 8-bit code can be directly provided
  """
  if name not in extendedColors:
    return name if name.isdigit() and is_rgb_valid([name]) else None

  return extendedColors[name]

def check_invalid_mode(mode: str):
  """
  Raises `ValueError` if mode is not a valid `ColorMode`
  """
  if mode not in get_args(ColorMode):
    raise ValueError(f"Color mode {mode} is not supported")

def unique(items: list) -> list:
  """
  Returns list of unique elements from items while\n
  preserving order of the list
  """
  visited = set()

  return [item for item in items if not (item in visited or visited.add(item))]
