import logging
from pytermstyle import basicConfig

SETTINGS = {
  "style": ["underline",  "bold"],
  "foreground": {"color": "sky-blue"},
  "background": {"rgb": [32, 87, 111]},
}

LOGGING_SETTINGS = {
  "DEBUG": SETTINGS,
  "ERROR": {
    **SETTINGS,
    "background": {"color": "dark-red"}
  }
}

if __name__ == "__main__":
  basicConfig(level=logging.DEBUG)

  logging.debug("Default debug styling") 
  logging.info("Default info styling")
  logging.warning("Default warning styling")
  logging.error("Default error styling")

  basicConfig(format="%(colorStart)s%(levelname)s:%(name)s:%(message)s%(colorEnd)s")
  print()

  logging.debug("Custom debug format") 
  logging.info("Custom info format")
  logging.warning("Custom warning format")
  logging.error("Custom error format")

  basicConfig(settings=LOGGING_SETTINGS)
  print()

  logging.debug("Custom debug styling") 
  logging.info("Default info styling")
  logging.warning("Default warning styling")
  logging.error("Custom error styling")