from pytermstyle import get_default_logger


if __name__ == "__main__":
  logger = get_default_logger()

  logger.fg_color("red").bg_color("cyan", text="Basic colors")
  logger.fg_color("black").bg_color("white", text="Basic colors")
  logger.fg_color("green").bg_color("magenta", text="Basic colors")
  logger.fg_color("yellow").bg_color("blue", text="Basic colors")
  logger.fg_color("blue").bg_color("yellow", text="Basic colors")
  logger.fg_color("magenta").bg_color("green", text="Basic colors")
  logger.fg_color("white").bg_color("black", text="Basic colors")
  logger.fg_color("cyan").bg_color("red", text="Basic colors")

  """ Additional colors available through this method """
  logger()

  logger.fg_color("dark-red", text="Dark Red")
  logger.fg_color("dark-green", text="Dark Green")
  logger.fg_color("dark-blue", text="Dark Blue")
  logger.fg_color("light-red", text="Light Red")
  logger.fg_color("light-green", text="Light Green")
  logger.fg_color("light-blue", text="Light Blue")
  logger.fg_color("pink", text="Pink")
  logger.fg_color("orange", text="Orange")
  logger.fg_color("purple", text="Purple")
  logger.fg_color("brown", text="Brown")
  logger.fg_color("sky-blue", text="Sky Blue")
  logger.fg_color("lime-green", text="Lime Green")

  """ RGB """
  logger()

  logger.fg_rgb(61, 217, 187).bg_rgb(32, 87, 111, text="RGB Message")
