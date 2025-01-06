# pytermstyle

[![PyPI version](https://img.shields.io/pypi/v/pytermstyle.svg)](https://pypi.org/project/pytermstyle/)
[![License](https://img.shields.io/pypi/l/pytermstyle.svg)](https://pypi.org/project/pytermstyle/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytermstyle.svg)](https://pypi.org/project/pytermstyle)

<img src="media/description.PNG" alt="pytermstyle">

Python module that enables ANSI color formatting for output in terminal

## Installation

```
python3 -m pip install --upgrade pytermstyle
```

## Documentation

You can acquire logger by using any of the following methods:

**Acquire default logger provided on import**
```python
from pytermstyle import get_default_logger

logger = get_default_logger()

logger("Hello World!") # Equivalent to print
logger.bold("Hello World!")
```

**Acquire default logger with optional configuration**
```python
from pytermstyle import init_config

logger = init_config()

logger.bold("Hello World!")
```
For details on how to configure logger, visit [Settings](https://github.com/SpotRusherZ/pytermstyle/blob/main/README.md#settings---persistent-styling) section

**Create and configure custom instance of colored logger**
```python
from pytermstyle import create_logger

logger = create_logger()

logger.bold("Hello World!")
```

Module supports different ways to style the output:
* Basic Styling: Predefined common styles like bold, italic, underline, and strikethrough
* Background & Foreground Colors: Predefined and RGB colors

By default, logger will behave like regular `print` function, until user defines either:
1) Persistent styling - Define [settings](https://github.com/SpotRusherZ/pytermstyle/blob/main/README.md#settings---persistent-styling) for your instance of the logger that will behave as a new default for logger
2) Single-use styling - Directly call supported styling methods on logging. This way of logging will override any predefined settings for the given call

### Chaining Styles - Single-use styling

To apply styling to one output line, call as many predefined styles methods as you like
All previously called styles will be applied first time when you specify output text

```python
from pytermstyle import get_default_logger

logger = get_default_logger()

logger.bold().italic().underline().bg_cyan().fg_red("Styled text")
logger("Regular text")
logger.fg_blue().bg_yellow().strike("Styled text")
```

There is no limit to the amount of styling methods that you can use, if you specify multiple foreground/background colors **last called color method will be applied**

```python
logger.fg_magenta().bg_green().fg_yellow("Styled text") # Text will have green background & yellow foreground, magenta will be ignored
```

Additionally, since styling will be preserved until the first time when user specifies output, you can delay applying styles:
```python
logger.bg_cyan().fg_red() # Logger will not output anything

logger("Styled text") # Logger will output text with cyan background and red foreground
```

### Supported styles

* bold()
* faint()
* italic()
* underline()
* slow_blink()
* rapid_blink()
* conceal()
* strike()
* framed()
* encircled()
* overlined()

**Note:** Depending on terminal, not every styling that module offers is promised to be supported.

### Predefined colors

| Color   | Background   | Foreground   | HEX       |
| :------ | :----------- | :----------- | :-------- |
| black   | bg_black()   | fg_black()   | `#000000` |
| red     | bg_red()     | fg_red()     | `#FF0000` |
| green   | bg_green()   | fg_green()   | `#00FF00` |
| yellow  | bg_yellow()  | fg_yellow()  | `#FFFF00` |
| blue    | bg_blue()    | fg_blue()    | `#0000FF` |
| magenta | bg_magenta() | fg_magenta() | `#FF00FF` |
| cyan    | bg_cyan()    | fg_cyan()    | `#00FFFF` |
| white   | bg_white()   | fg_white()   | `#FFFFFF` |

### Custom colors

Module offers wider set of defined colors accessible through `fg_color` & `bg_color`.

```python
logger.fg_color("red", text="Styled text")
logger.bg_color("blue", text="Styled text")
```

**Note:** `logger.fg_red("Example")` and `logger.fg_color("red", text="Example")` yield same result

Defined set of colors that can be used as a color name for these two methods:
| Color       | HEX       | 8-bit Code |
| ----------- | --------- | ---------- |
| black       | `#000000` | 0          |
| red         | `#800000` | 1          |
| green       | `#008000` | 2          |
| yellow      | `#808000` | 3          |
| blue        | `#000080` | 4          |
| magenta     | `#800080` | 5          |
| cyan        | `#008080` | 6          |
| white       | `#C0C0C0` | 7          |
| dark-red    | `#870000` | 88         |
| dark-green  | `#005F00` | 22         |
| dark-blue   | `#000087` | 18         |
| light-red   | `#FF0000` | 196        |
| light-green | `#87FF87` | 120        |
| light-blue  | `#5FD7FF` | 81         |
| pink        | `#FF00FF` | 13         |
| orange      | `#FFAF00` | 214        |
| purple      | `#8700FF` | 93         |
| brown       | `#875F00` | 94         |
| sky-blue    | `#AFD7FF` | 153        |
| lime-green  | `#AFFF87` | 156        |

**Note:** Since implementation of these two methods returns 8-bit representation of specified colors, color code in range [0, 255] will also be accepted input. See [ANSI Escape Codes - 8-bit](https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit) for more details

### RGB Colors

To define colors as RGB, you can use `fg_rgb()` and `bg_rgb()` methods in format:

```python
fg_rgb(r: int, g: int, b: int, text: Optional[str])
bg_rgb(r: int, g: int, b: int, text: Optional[str])
```

```python
logger.fg_rgb(61, 217, 187).bg_rgb(32, 87, 111, text="RGB Message")
```

### Settings - Persistent styling

In case where user would like to keep one styling for most of the output, styling can be defined through settings and logger can be configured to use these settings at any point in code execution.

Settings can be defined as Python dictionary in following format:
```python
{
  "style": {
    "type": "list[str]",
    "description": "List of valid font styles",
    "required": "false"
  },
  "foreground": {
    "type": "string" | "list[str]",
    "description": "Valid supported color / 8-bit color code or RGB value"
    "oneOf": {
      "color": "string",
      "rgb": "list[str]"
    },
    "required": "false"
  },
  "background": {
    "type": "string" | "list[str]",
    "description": "Valid supported color / 8-bit color code or RGB value"
    "oneOf": {
      "color": "string",
      "rgb": "list[str]"
    },
    "required": "false"
  },
}
```

Example:
```python
from pytermstyle import init_config

SETTINGS = {
  "style": ["bold", "italic", "underline"],
  "foreground": {
    "rgb": ["61", "217", "217"],
  },
  "background": {
    "color": "magenta"
  },
}

logger = init_config(SETTINGS)

logger("Text with styling defined through settings")
logger("which behaves as default styling")

logger.bold("Calling styling methods directly will overwrite these settings")

logger("After which settings will be applied again.")
```

If user wishes to remove the settings from the logger, `clear()` method should be called
```python
logger = init_config({ "style": ["bold"] })

logger("Custom styling")
logger.clear()
logger("Behaves as regular print again")
```

User can also configure logger to use settings at any point in execution, by calling `configure()` method
```python
logger = init_config()

logger("Regular print")

logger.configure({ "style": ["bold"] })
logger("Bold text")
```

### (NO_)COLOR mode

Implementation of this module surrounds output text with proper ANSI escape codes recognized by terminal
Since there are many different terminal applications, not all of them will support every standard ANSI escape code defined in the module, or will not suport ANSI escape codes at all

This module will try to recognize if terminal does not support ANSI Escape codes, or if user specified in any standardized way that terminal shouldn't accept them.
If one of the following environment variables exists, logger will strip any ANSI color codes from the output and behave as regular `print` function:
* [NO_COLOR](https://no-color.org/)
* ANSI_COLORS_DISABLED
* TERM = "dumb"

If [FORCE_COLOR](https://force-color.org/) environment variable exists, logger will attempt colored output.

### Exception Handling

`ColorException` - Thrown by `fg_color` / `bg_color` / `fg_rgb` / `bg_rgb` if validation for provided input fails

`TermConfigException` - Thrown by settings if provided configuration failed validation

### `logging` integration

This module can work with Python `logging` module by exposing `TermStyleFormatter` class, and `basicConfig()` method.

Example:
```python
import logging
from pytermstyle import basicConfig

basicConfig(level=logging.DEBUG)

logging.debug("Default debug styling") 
logging.info("Default info styling")
logging.warning("Default warning styling")
logging.error("Default error styling")
```

If you want to use colors for a specific instance of logger, use `TermStyleFormatter`, a provided subclass of `logging.Formatter`

For both methods of configuration, there is already defined styling for each logging level, if you wish to override default settings, you can provide custom settings object.
Settings object behaves in a same way as [settings](https://github.com/SpotRusherZ/pytermstyle/blob/main/README.md#settings---persistent-styling), with addition being able to specify each level as a key:

```python
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

basicConfig(settings=LOGGING_SETTINGS)

logging.debug("Custom debug styling") 
logging.info("Default info styling")
logging.warning("Default warning styling")
logging.error("Custom error styling")
```

`logging` module also provides formatting of log message, which `pytermstyle` expands with two additional attributes: `colorStart` & `colorEnd`, which can define part of the log message which will be styled:

```python
# Whole log message should be styled
# Default formatting is: %(colorStart)s%(levelname)s:%(name)s:%(colorEnd)s%(message)s
basicConfig(format="%(colorStart)s%(levelname)s:%(name)s:%(message)s%(colorEnd)s")

logging.debug("Custom debug format") 
logging.info("Custom info format")
logging.warning("Custom warning format")
logging.error("Custom error format")
```

### Examples

For complete code examples visit: [examples](https://github.com/SpotRusherZ/pytermstyle/tree/main/examples) directory
