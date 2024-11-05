import pytest
import logging

@pytest.fixture
def texts():
  return {
    # Settings
    "invalidStyle": "Invalid styles: unknown",
    "invalidColor": "Color unknown is not supported.",
    "invalidMode": "Color mode unknown is not supported",
    "mutuallyExclusive": '"rgb" and "color" properties are mutually exclusive.',
    "wrongRGBSize": '"rgb" field must be a list in format: [r, g, b]',
    "wrongRGBFormat": "Provided values for RGB must be 0 <= color <= 255",

    # TermStyle
    "message": "Colored logger message",
    "invalidColorValue": "Invalid value for color: unknown",

    # Logger
    "startBaseFormat": "\033[1;3;4;38;2;61;217;217;48;5;5m",
    "endBaseFormat": "\033[0m",
  }

@pytest.fixture
def colored():
  return {
    "style": "\033[{}mColored logger message\033[0m",
    "foreground": "\033[38;5;{}mColored logger message\033[0m",
    "background": "\033[48;5;{}mColored logger message\033[0m",
    "foregroundRGB": "\033[38;2;{}mColored logger message\033[0m",
    "backgroundRGB": "\033[48;2;{}mColored logger message\033[0m",
    "baseChainedColors": "\033[9;38;5;4;48;5;3mColored logger message\033[0m",
    "rgbChainedColors": "\033[38;2;61;217;187;48;2;32;87;111mColored logger message\033[0m",
    "foregroundPrecedence": "\033[38;2;61;217;187mColored logger message\033[0m",
    "backgroundPrecedence": "\033[48;2;61;217;187mColored logger message\033[0m",
    "defaultSettings": "\033[1;3;4;38;2;61;217;217;48;5;5mColored logger message\033[0m",
    "configuredSettings": "\033[1;38;2;61;217;217;48;5;5mColored logger message\033[0m",
    "defaultLoggerSettings": "\033[38;5;2mINFO:MockRecord:\033[0mColored logger message",
    "customLoggerSettings": "\033[1mINFO:MockRecord:\033[0mColored logger message",
    "customFormatMessage": "\033[38;5;2mINFO:MockRecord:Colored logger message\033[0m",
  }

def newline(text: str):
  return f"{text}\n"

valid_rgbs = [
  ['61', '217', '187'],
  ['1', '0', '230'],
  ['255', '255', '255']
]

invalid_rgbs = [
  ['unknown', '-10', '259'],
  ['-1', '5', '123'],
  ['61', '217', '256'],
  ['a', '32', '57'],
]

@pytest.fixture
def mock_settings_config():
  return {
    "style": [
      "bold",
      "italic",
      "underline",
    ],
    "foreground": {
      "rgb": ["61", "217", "217"],
    },
    "background": {
      "color": "magenta"
    },
  }

@pytest.fixture
def mock_record() -> logging.LogRecord:
  return logging.LogRecord(
    name="MockRecord",
    level=logging.INFO,
    pathname="",
    lineno=34,
    msg="Colored logger message",
    args=None,
    exc_info=None
  )
