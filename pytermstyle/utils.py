from typing import Optional

from .custom_types import ColorMode, Color
from .definitions import baseColors, extendedColors

def is_rgb_valid(rgb: list[str]) -> bool:
  """
  Returns True if all values are valid RGB code
  """
  return all(0 <= int(color) <= 255 for color in rgb)

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
