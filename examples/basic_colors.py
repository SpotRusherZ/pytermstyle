from pytermstyle import get_default_logger


if __name__ == "__main__":
  logger = get_default_logger()

  logger.fg_red().bg_cyan("Basic Colors")
  logger.fg_black().bg_white("Basic Colors")
  logger.fg_green().bg_magenta("Basic Colors")
  logger.fg_yellow().bg_blue("Basic Colors")
  logger.fg_blue().bg_yellow("Basic Colors")
  logger.fg_magenta().bg_green("Basic Colors")
  logger.fg_white().bg_black("Basic Colors")
  logger.fg_cyan().bg_red("Basic Colors")
