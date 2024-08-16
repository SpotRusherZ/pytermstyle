from __future__ import annotations

from typing import Any, Optional

from .custom_types import TextStyle, ColorMode, Color, Colors
from .definitions import base, reset, textStyles
from .utils import is_rgb_valid, get_4bit_color_code, get_8bit_color_code

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
  DEFAULT_FG_RGB = ["38", "2"]
  DEFAULT_BG_RGB = ["48", "2"]
  DEFAULT_FG_COLOR = ["38", "5"]
  DEFAULT_BG_COLOR = ["48", "5"]

  def __init__(self) -> None:
    self._styles: set[TextStyle] = set()
    self._fg_color: Optional[str] = None
    self._bg_color: Optional[str] = None
    self._fg_8bit_color: list[str] = list(TermStyle.DEFAULT_FG_COLOR)
    self._bg_8bit_color: list[str] = list(TermStyle.DEFAULT_BG_COLOR)
    self._fg_rgb: list[str] = list(TermStyle.DEFAULT_FG_RGB)
    self._bg_rgb: list[str] = list(TermStyle.DEFAULT_BG_RGB)

  def add_style(self, style: TextStyle):
    self._styles.add(style)

  def add_color(self, color: Color, mode: ColorMode):
    color_code = get_4bit_color_code(color, mode)

    if mode == "background":
      self._bg_color = color_code
    else:
      self._fg_color = color_code
  
  def print(self, text: Optional[str], clear: bool = True, **kwargs):
    if text:
      styles = ";".join([textStyles[style] for style in self._styles])

      foreground = self._fg_color
      if not foreground:
        foreground = ";".join(self._fg_8bit_color) if len(self._fg_8bit_color) > 2 else None
      if not foreground:
        foreground = ";".join(self._fg_rgb) if len(self._fg_rgb) > 2 else None

      background = self._bg_color
      if not background:
        background = ";".join(self._bg_8bit_color) if len(self._bg_8bit_color) > 2 else None
      if not background:
        background = ";".join(self._bg_rgb) if len(self._bg_rgb) > 2 else None

      fmt = ";".join([style for style in [styles, foreground, background] if style])

      fmt_text = "{base}{fmt}m{text}{reset}".format(
        base=base,
        fmt=fmt,
        text=text,
        reset=reset
      )

      print(fmt_text, **kwargs)

    if clear:
      self.reset()

    return self
  
  def __call__(self, *args: Any, **kwds: Any) -> Any:
    return self.print(*args, **kwds)

  def _output(self, text: Optional[str] = None, clear: bool = True, **kwargs):
    if not text:
      return self

    return self.print(text, clear, **kwargs)
  
  def reset(self):
    self._styles = set()
    self._bg_color = None
    self._fg_color = None
    self._fg_rgb = list(TermStyle.DEFAULT_FG_RGB)
    self._bg_rgb = list(TermStyle.DEFAULT_BG_RGB)
    self._fg_8bit_color = list(TermStyle.DEFAULT_FG_COLOR)
    self._bg_8bit_color = list(TermStyle.DEFAULT_BG_COLOR)
  
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
    color_code = get_8bit_color_code(color)

    if not color_code:
      raise ColorException("Invalid value for color: {}".format(color))

    self._fg_8bit_color.append(color_code)
    return self._output(text, clear, **kwargs)
  
  def bg_color(self, color: Colors, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    color_code = get_8bit_color_code(color)

    if not color_code:
      raise ColorException("Invalid value for color: {}".format(color))

    self._bg_8bit_color.append(color_code)
    return self._output(text, clear, **kwargs)

  """16-bit RGB"""
  def fg_rgb(self, r: int, g: int, b: int, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    rgb = [str(r), str(g), str(b)]

    if not is_rgb_valid(rgb):
      raise ColorException("Provided values for RGB must be 0 <= color <= 255")
    
    self._fg_rgb.extend(rgb)
    return self._output(text, clear, **kwargs)
  
  def bg_rgb(self, r: int, g: int, b: int, *, text: Optional[str] = None, clear: bool = True, **kwargs):
    rgb = [str(r), str(g), str(b)]

    if not is_rgb_valid(rgb):
      raise ColorException("Provided values for RGB must be 0 <= color <= 255")

    self._bg_rgb.extend(rgb)
    return self._output(text, clear, **kwargs)

_root: Optional[TermStyle] = None

def init_root():
  global _root

  if not _root:
    _root = TermStyle()

  return _root