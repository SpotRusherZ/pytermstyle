from __future__ import annotations

import os
import sys
from typing import Any, Optional

from .custom_types import TextStyle, ColorMode, Color, Colors
from .definitions import BASE, RESET, FG_RGB_CODE, BG_RGB_CODE, FG_COLOR_CODE, BG_COLOR_CODE, textStyles
from .settings import TermSettings, Settings
from .utils import is_rgb_valid, get_8bit_color_code, is_valid_color

"""ANSI color formatting for output in terminal."""

__all__ = [
  'ColorException', 'TermStyle', 'get_default_logger',
  'init_config', 'create_logger'
]

class ColorException(Exception):
  pass

def _make_style_method(name):
    def style_method(
      self: TermStyle,
      text: Optional[str] = None,
      *,
      clear = True,
      **kwargs
    ):
      self.add_style(name)

      return self._output(text, clear, **kwargs)
    
    return style_method

def _make_color_method(name, mode: ColorMode):
    def color_method(
      self: TermStyle,
      text: Optional[str] = None,
      *,
      clear = True,
      **kwargs
    ):
      self.add_color(name, mode)

      return self._output(text, clear, **kwargs)
    
    return color_method

class TermStyle:
  """
  Colored logger implementation.

  By default it acts as a normal print function. \n
  User can override this behavior by using either:
   * Exposed methods for styling / color.
     These methods can be chained to produce desired output

     e.g `logger.bold().fg_red().bg_cyan("Colored Text")`

     Once the text to output is provided to a method, chain will stop,
     text will be printed to output and logger will return to default settings

   * Providing settings which will act as logger default.
     Settings can be provided as dictionary with format explained in settings.TermSettings

     After providing settings, logger can be called directly:

     e.g. `logger("Colored text")`

  If a user calls methods for styling / color directly, they will override any existing settings\n
  Once logger outputs text with overridden styling / color, \n
  it will return to configured settings as a default behavior
  """
  def __init__(self, settings: Optional[Settings] = None) -> None:
    self._default_settings = TermSettings(settings)
    self._override_settings = TermSettings()

  def configure(self, settings: Optional[Settings] = None):
    """
    Used to configure new settings for logger
    """
    self._default_settings = TermSettings(settings)

  def add_style(self, style: TextStyle):
    self._override_settings.add_style(style)

  def add_color(self, color: Color, mode: ColorMode):
    self._override_settings.add_color(color, mode)

  def _set_color_code(self, settings: TermSettings, mode: ColorMode) -> Optional[str]:
    color = settings.rgb(mode)
    if color:
      rgb_code = FG_RGB_CODE if mode == "foreground" else BG_RGB_CODE
      return ";".join(rgb_code + color)

    color = settings.color(mode)
    if color:
      base_code = FG_COLOR_CODE if mode == "foreground" else BG_COLOR_CODE
      color_code = get_8bit_color_code(color)

      if color_code:
        return ";".join(base_code + [color_code])

    return None

  def _no_color(self) -> bool:
    """
    Support for NO_COLOR mode that can be controlled by environment variables\n
    If one of the following variables exists, or if standard output is not terminal,\n
    logger will strip any ANSI color codes from the output and behave as regular `print function`:
     * NO_COLOR
     * ANSI_COLORS_DISABLED
     * TERM = "dumb"

    If FORCE_COLOR environment variable exists, logger will attempt colored output.
    """
    disable_env = [
      "NO_COLOR",
      "ANSI_COLORS_DISABLED"
    ]

    if any(env_var in os.environ for env_var in disable_env):
      return True

    if "FORCE_COLOR" in os.environ:
      return False

    if os.environ.get("TERM") == "dumb":
      return True

    return not sys.stdout.isatty()

  def get_base_format(self):
    settings = self._override_settings \
      if self._override_settings.has_settings() \
      else self._default_settings

    styles = ";".join([textStyles[style] for style in settings.styles()])
    foreground = self._set_color_code(settings, "foreground")
    background = self._set_color_code(settings, "background")

    fmt = ";".join([style for style in [styles, foreground, background] if style])

    return f"{BASE}{fmt}m" if fmt else ""

  def print(self, text: Optional[str], clear: bool = True, **kwargs):
    if text:
      fmt_text = text

      if not self._no_color():
        fmt = self.get_base_format()

        fmt_text = "{fmt}{text}{reset}".format(
          fmt=fmt,
          text=text,
          reset=RESET
        ) if fmt else fmt_text

      print(fmt_text, **kwargs)

    if clear:
      self._override_settings.clear()

    return self

  def clear(self):
    """
    Can be used to clear any previously configured settings
    """
    self._default_settings.clear()
  
  def __call__(self, *args: Any, **kwds: Any) -> Any:
    if not args and not kwds:
      kwds = { "text": "\n", "end": "" }

    return self.print(*args, **kwds)

  def _output(self, text: Optional[str] = None, clear: bool = True, **kwargs):
    if not text:
      return self

    return self.print(text, clear, **kwargs)
  
  """ Public Methods for font styling"""
  bold = _make_style_method("bold")
  faint = _make_style_method("faint")
  italic = _make_style_method("italic")
  underline = _make_style_method("underline")
  slow_blink = _make_style_method("slow_blink")
  rapid_blink = _make_style_method("rapid_blink")
  conceal = _make_style_method("conceal")
  strike = _make_style_method("strike")
  framed = _make_style_method("framed")
  encircled = _make_style_method("encircled")
  overlined = _make_style_method("overlined")

  """Public 4-bit predefined Colors"""
  bg_black = _make_color_method("black", "background")
  bg_red = _make_color_method("red", "background")
  bg_green = _make_color_method("green", "background")
  bg_yellow = _make_color_method("yellow", "background")
  bg_blue = _make_color_method("blue", "background")
  bg_magenta = _make_color_method("magenta", "background")
  bg_cyan = _make_color_method("cyan", "background")
  bg_white = _make_color_method("white", "background")

  fg_black = _make_color_method("black", "foreground")
  fg_red = _make_color_method("red", "foreground")
  fg_green = _make_color_method("green", "foreground")
  fg_yellow = _make_color_method("yellow", "foreground")
  fg_blue = _make_color_method("blue", "foreground")
  fg_magenta = _make_color_method("magenta", "foreground")
  fg_cyan = _make_color_method("cyan", "foreground")
  fg_white = _make_color_method("white", "foreground")

  """Public Extended Colors"""
  def fg_color(self, color: Colors, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    if not is_valid_color(color):
      raise ColorException("Invalid value for color: {}".format(color))

    self._override_settings.add_color(color, "foreground")
    return self._output(text, clear, **kwargs)
  
  def bg_color(self, color: Colors, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    if not is_valid_color(color):
      raise ColorException("Invalid value for color: {}".format(color))

    self._override_settings.add_color(color, "background")
    return self._output(text, clear, **kwargs)

  """Public 16-bit RGB"""
  def fg_rgb(self, r: int, g: int, b: int, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    rgb = [str(r), str(g), str(b)]

    if not is_rgb_valid(rgb):
      raise ColorException("Provided values for RGB must be 0 <= color <= 255")
    
    self._override_settings.add_rgb(rgb, "foreground")
    return self._output(text, clear, **kwargs)
  
  def bg_rgb(self, r: int, g: int, b: int, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    rgb = [str(r), str(g), str(b)]

    if not is_rgb_valid(rgb):
      raise ColorException("Provided values for RGB must be 0 <= color <= 255")

    self._override_settings.add_rgb(rgb, "background")
    return self._output(text, clear, **kwargs)


_root = TermStyle()

def get_default_logger():
  """
  Can be used to acquire default colored logger
  """
  return _root

def init_config(settings: Optional[Settings] = None):
  """
  Can be used to acquire and configure default colored logger
  """
  _root.configure(settings)

  return _root

def create_logger(settings: Optional[Settings] = None):
  """
  Can be used to create and configure custom instance of colored logger
  """
  logger = TermStyle(settings)

  return logger
