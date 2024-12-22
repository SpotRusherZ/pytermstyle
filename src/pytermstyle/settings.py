from __future__ import annotations

import copy

from typing import Optional, Union

from .custom_types import TermOptions, ColorOptions, TextStyle, Colors, ColorMode
from .definitions import textStyles, extendedColors
from .utils import is_rgb_valid, check_invalid_mode, unique

__all__ = [
  'TermConfigException', 'TermSettings'
]

Settings = Union[TermOptions, dict]


class TermConfigException(Exception):
  pass


class TermSettings:
  """
  Represents color settings that can be passed to logger and used as default.\n
  These settings can be passed to a constructor as a dictionary in following format:

   {
    "style": {
      "type": "list[str]",
      "description": "List of valid font styles",
      "required": "false"
    },
    "foreground": {
      "type": "string" | "list[str]",
      "description": "Valid supported color / 8-bit color code or RGB value"
      "oneOf": {
        "color": "string",
        "rgb": "list[str]"
      },
      "required": "false"
    },
    "background": {
      "type": "string" | "list[str]",
      "description": "Valid supported color / 8-bit color code or RGB value"
      "oneOf": {
        "color": "string",
        "rgb": "list[str]"
      },
      "required": "false"
    },
  }

  Example:

   {
    "style": ["bold", "italic", "underline"],
    "foreground": {
      "rgb": ["61", "217", "217"],
    },
    "background": {
      "color": "magenta"
    },
  }
  """
  def __init__(self, settings: Optional[Settings] = None) -> None:
    """
    `TermConfigException` exception will be thrown if passed settings\n
    are not in valid format.
    """
    self._settings = copy.deepcopy(settings) if settings else TermOptions()
    self._verify_settings(self._settings)

  def has_settings(self) -> bool:
    if not self._settings:
      return False

    return any(val for val in self._settings.values())

  def clear(self):
    self._settings = {}

  """ Getters """
  def styles(self) -> list[TextStyle]:
    return unique(self._settings.get("style", []))

  def color(self, mode: ColorMode) -> Optional[str]:
    if mode in self._settings:
      return self._settings[mode].get("color")  # type: ignore

    return None

  def rgb(self, mode: ColorMode) -> Optional[list[str]]:
    if mode in self._settings:
      return self._settings[mode].get("rgb")  # type: ignore

    return None

  """ Setters """
  def add_style(self, style: TextStyle):
    error = self._verify_styles([style])
    if error:
      raise TermConfigException(error)

    self._settings.setdefault("style", []).append(style)

  def add_color(self, color: Colors, mode: ColorMode):
    check_invalid_mode(mode)
    color_to_add = ColorOptions({"color": color})

    error = self._verify_colors(color_to_add)
    if error:
      raise TermConfigException(error)

    self._settings[mode] = color_to_add

  def add_rgb(self, rgb: list[str], mode: ColorMode):
    check_invalid_mode(mode)
    rgb_to_add = ColorOptions({"rgb": rgb})

    error = self._verify_colors(rgb_to_add)
    if error:
      raise TermConfigException(error)

    self._settings[mode] = rgb_to_add

  """ Verification utilities """
  def _verify_settings(self, settings: Settings):
    errors: list[str] = []

    style_message = self._verify_styles(settings.get("style"))
    if style_message:
      errors.append(style_message)

    for mode in ["foreground", "background"]:
      message = self._verify_colors(settings.get(mode))  # type: ignore
      if message:
        errors.append(message)

    if errors:
      raise TermConfigException(self._format_errors(errors))

  def _verify_styles(self, styles: Optional[list[TextStyle]]) -> Optional[str]:
    if not styles:
      return None

    not_found = set(styles).difference(set(textStyles.keys()))
    if not not_found:
      return None

    return "Invalid styles: {}".format(
      ", ".join(not_found)
    )

  def _verify_colors(self, colors: Optional[ColorOptions]) -> Optional[str]:
    if not colors:
      return None

    if "color" in colors and "rgb" in colors:
      return '"rgb" and "color" properties are mutually exclusive.'

    if "color" in colors and colors["color"] not in extendedColors:
      return 'Color {color} is not supported.'.format(
        color=colors["color"]
      )

    if "rgb" in colors:
      if len(colors["rgb"]) != 3:
        return '"rgb" field must be a list in format: [r, g, b]'

      if not is_rgb_valid(colors["rgb"]):
        return "Provided values for RGB must be 0 <= color <= 255"

    return None

  def _format_errors(self, errors: list[str]) -> str:
    return "Configuration errors: [{}]".format(
      ", ".join(errors)
    )

  def __repr__(self) -> str:
    return repr(self._settings)
