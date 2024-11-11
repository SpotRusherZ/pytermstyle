from pytermstyle import init_config

SETTINGS = {
  "style": [
    "underline",
    "bold",
  ],
  "foreground": {
    "color": "sky-blue"
  },
  "background": {
    "rgb": [32, 87, 111]
  },
}

if __name__ == "__main__":
  logger = init_config(SETTINGS)

  logger("Logger with predefined settings")
  logger("That will be used by default logger call")

  logger.fg_green().bg_white().bold("Calling styling methods directly will overwrite these settings")

  logger("After which defaults will be applied again.")

  logger.clear()

  logger("Calling `clear()` will remove any custom settings")

  logger.configure(SETTINGS)
  logger("User can configure new settings at any point by calling `configure()` method")
