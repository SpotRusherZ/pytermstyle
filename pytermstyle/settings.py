from __future__ import annotations

import copy

from typing import Optional, Union

from .custom_types import TermOptions, ColorOptions
from .definitions import textStyles, extendedColors
from .utils import is_rgb_valid

_Settings = Union[TermOptions, dict]

class TermConfigException(Exception):
  pass

class TermSettings:
  def __init__(self, settings: Optional[_Settings] = None) -> None:
    self._settings = copy.deepcopy(settings) if settings else TermOptions()
    self._verify_settings(self._settings)

  def _verify_settings(self, settings: _Settings):
    errors: list[str] = []

    style_message = self._verify_styles(settings.get("style"))
    if style_message:
      errors.append(style_message)

    for mode in ["foreground", "background"]:
      message = self._verify_colors(settings.get(mode))
      if message:
        errors.append(message)
    
    if errors:
      raise TermConfigException(self._format_errors(errors))

  def _verify_styles(self, styles: Optional[list[str]]) -> Optional[str]:
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
