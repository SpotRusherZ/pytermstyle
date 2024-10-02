import logging

from .definitions import RESET
from .pytermstyle import TermStyle

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
  def __init__(self, *args, settings = None, **kwargs):
    super().__init__(*args, **kwargs)

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
