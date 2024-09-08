from __future__ import annotations

from typing import Any, Optional

from .custom_types import TextStyle, ColorMode, Color, Colors
from .definitions import BASE, RESET, FG_RGB_CODE, BG_RGB_CODE, FG_COLOR_CODE, BG_COLOR_CODE, textStyles
from .settings import TermSettings, Settings
from .utils import is_rgb_valid, get_8bit_color_code, is_valid_color

"""ANSI color formatting for output in terminal."""

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
  def __init__(self, settings: Optional[Settings] = None) -> None:
    self._default_settings = TermSettings(settings)
    self._override_settings = TermSettings()

  def configure(self, settings: Optional[Settings] = None):
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

  def print(self, text: Optional[str], clear: bool = True, **kwargs):
    if text:
      settings = self._override_settings \
        if self._override_settings.has_settings() \
        else self._default_settings

      styles = ";".join([textStyles[style] for style in settings.styles()])
      foreground = self._set_color_code(settings, "foreground")
      background = self._set_color_code(settings, "background")

      fmt = ";".join([style for style in [styles, foreground, background] if style])

      fmt_text = "{base}{fmt}m{text}{reset}".format(
        base=BASE,
        fmt=fmt,
        text=text,
        reset=RESET
      )

      print(fmt_text, **kwargs)

    if clear:
      self._override_settings.clear()

    return self
  
  def __call__(self, *args: Any, **kwds: Any) -> Any:
    return self.print(*args, **kwds)

  def _output(self, text: Optional[str] = None, clear: bool = True, **kwargs):
    if not text:
      return self

    return self.print(text, clear, **kwargs)
  
  """Methods for styling"""
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

  """4-bit Colors"""
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

  """Extended Colors"""
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

  """16-bit RGB"""
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
  return _root

def init_config(settings: Optional[Settings] = None):
  _root.configure(settings)

  return _root

def create_logger(settings: Optional[Settings] = None):
  logger = TermStyle(settings)

  return logger
