import logging

from typing import Literal, Optional

from .definitions import RESET
from .pytermstyle import TermStyle

__all__ = [
  'TermStyleRecord', 'TermStyleFormatter', 'basicConfig'
]

DEFAULT_SETTINGS = {
  "DEBUG": { "foreground": { "color": "light-blue" } },
  "INFO": { "foreground": { "color": "green" } },
  "WARNING": { "foreground": { "color": "yellow" } },
  "ERROR": { "foreground": { "color": "red" } },
  "CRITICAL": {
    "styles": ["bold"],
    "foreground": { "color": "red" }
  },
}

_Style = Literal["%", "{", "$"]

BASE_STYLES = {
    '%': "%(colorStart)s%(levelname)s:%(name)s:%(colorEnd)s%(message)s",
    '{': '{colorStart}{levelname}:{name}:{colorEnd}{message}',
    '$': '${colorStart}${levelname}:${name}:${colorEnd}${message}',
}

class TermStyleRecord:
  def __init__(self, record: logging.LogRecord, term_style: TermStyle) -> None:
    self.__dict__.update(record.__dict__)
    self.colorStart = self.get_level_color(term_style)
    self.colorEnd = RESET if self.colorStart else ""

  def get_level_color(self, term_style: TermStyle):
    if term_style._no_color():
      return ""

    return term_style.get_base_format()


class TermStyleFormatter(logging.Formatter):
  """
  Custom formatter that can be used for integration with logging module.

  User can specify custom settings or rely on default colored settings.

  Format of settings dictionary that can be passed to formatter is: \n
  "loggingLevel" - settings.TermSettings

  e.g. `"{ INFO": { "foreground": { "color": "green" } } }`

  Logging Levels not specified in custom settings will use predefined default settings.

  ---

  User can choose which portion of logging output will be colored by surrounding that\n
  portion in format with `colorStart` and `colorEnd` attributes.

  e.g. `%(colorStart)s%(levelname)s:%(name)s:%(colorEnd)s%(message)s`
  """
  def __init__(
      self,
      fmt = None,
      datefmt = None,
      style: _Style = "%",
      *args,
      settings = None,
      **kwargs
  ):
    if not fmt:
      fmt = BASE_STYLES.get(style)

    super().__init__(fmt, datefmt, style, *args, **kwargs)

    self._stg = settings if settings else DEFAULT_SETTINGS
    self._term_styles = {
      level: TermStyle(stg) for level, stg in self._stg.items()
    }

  def formatMessage(self, record: logging.LogRecord) -> str:
    custom_style = self._term_styles.get(record.levelname)
    term_style = custom_style \
      if custom_style \
      else TermStyle(DEFAULT_SETTINGS[record.levelname])

    return super().formatMessage(TermStyleRecord(record, term_style)) # type: ignore

def basicConfig(
    format = "",
    style: _Style = "%",
    datefmt: Optional[str] = None,
    settings = None,
    **kwargs
):
  """
  Wrapper around logging.basicConfig method to quickly configure colored logging output

  `format` - Same as logging format, with addition of `colorStart` and `colorEnd` attributes\n
  which define portion of output which will be colored

  ---

  `settings` - Settings for colored output of logging levels.\n

  Format of settings dictionary that can be passed is: \n
  "loggingLevel" - settings.TermSettings

  e.g. `"{ INFO": { "foreground": { "color": "green" } } }`

  Logging Levels not specified in custom settings will use predefined default settings.
  """
  formatter = TermStyleFormatter(
    format,
    datefmt,
    style,
    settings=settings
  )

  logging.basicConfig(**kwargs)
  logging.root.handlers[0].setFormatter(formatter)
