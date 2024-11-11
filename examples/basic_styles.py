from pytermstyle import get_default_logger


if __name__ == "__main__":
  logger = get_default_logger()

  logger.bold("Bold")
  logger.faint("Faint")
  logger.italic("Italic")
  logger.underline("Underline")
  logger.slow_blink("Slow Blink")
  logger.rapid_blink("Rapid Blink")
  logger.conceal("Conceal")
  logger.strike("Strike")
  logger.framed("Framed")
  logger.encircled("Encircled")
  logger.overlined("Overlined")

  logger.bold().italic().overlined("Multiple Styles")
