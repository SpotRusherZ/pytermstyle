import pytest

from pytermstyle.pytermstyle import TermStyle, ColorException
from pytermstyle.definitions import textStyles, baseColors, extendedColors

from .conftest import newline, valid_rgbs, invalid_rgbs

class TestBasicStyles:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield

  def test__normal_output(self, capsys, texts):
    logger = TermStyle()

    logger(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(texts["message"])

  @pytest.mark.parametrize('method_info', textStyles.items())
  def test__style_output(self, capsys, texts, colored, method_info):
    logger = TermStyle()
    method_name, index = method_info

    style_method = getattr(logger, method_name)

    style_method(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["style"].format(index))
  
  @pytest.mark.parametrize('method_info', enumerate(baseColors))
  def test__4bit_fg_output(self, capsys, texts, colored, method_info):
    logger = TermStyle()
    index, color = method_info

    color_method = getattr(logger, f"fg_{color}")

    color_method(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["foreground"].format(index))
  
  @pytest.mark.parametrize('method_info', enumerate(baseColors))
  def test__4bit_bg_output(self, capsys, texts, colored, method_info):
    logger = TermStyle()
    index, color = method_info

    color_method = getattr(logger, f"bg_{color}")

    color_method(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["background"].format(index))


class TestExtendedColor:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield
  
  @pytest.mark.parametrize('color_info', extendedColors.items())
  def test__8bit_fg_output(self, capsys, texts, colored, color_info):
    logger = TermStyle()
    color, code = color_info

    logger.fg_color(color, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["foreground"].format(code))
  
  def test__invalid_8bit_fg_output(self, texts):
    logger = TermStyle()

    with pytest.raises(ColorException) as ce:
      logger.fg_color("unknown", text=texts["message"]) # type: ignore
    
    assert ce.type is ColorException
    assert str(ce.value) == texts["invalidColorValue"]
  
  @pytest.mark.parametrize('color_info', extendedColors.items())
  def test__8bit_bg_output(self, capsys, texts, colored, color_info):
    logger = TermStyle()
    color, code = color_info

    logger.bg_color(color, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["background"].format(code))
  
  def test__invalid_8bit_bg_output(self, texts):
    logger = TermStyle()

    with pytest.raises(ColorException) as ce:
      logger.bg_color("unknown", text=texts["message"]) # type: ignore
    
    assert ce.type is ColorException
    assert str(ce.value) == texts["invalidColorValue"]


class TestRGBColor:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield
  
  @pytest.mark.parametrize('rgb', valid_rgbs)
  def test__fg_rgb_output(self, capsys, texts, colored, rgb):
    logger = TermStyle()
    code = ";".join(rgb)

    logger.fg_rgb(*rgb, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["foregroundRGB"].format(code))
  
  @pytest.mark.parametrize('rgb', invalid_rgbs)
  def test__invalid_fg_rgb_output(self, texts, rgb):
    logger = TermStyle()

    with pytest.raises(ColorException) as ce:
      logger.fg_rgb(*rgb, text=texts["message"])
    
    assert ce.type is ColorException
    assert str(ce.value) == texts["wrongRGBFormat"]
  
  @pytest.mark.parametrize('rgb', valid_rgbs)
  def test__bg_rgb_output(self, capsys, texts, colored, rgb):
    logger = TermStyle()
    code = ";".join(rgb)

    logger.bg_rgb(*rgb, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["backgroundRGB"].format(code))
  
  @pytest.mark.parametrize('rgb', invalid_rgbs)
  def test__invalid_bg_rgb_output(self, texts, rgb):
    logger = TermStyle()

    with pytest.raises(ColorException) as ce:
      logger.bg_rgb(*rgb, text=texts["message"])
    
    assert ce.type is ColorException
    assert str(ce.value) == texts["wrongRGBFormat"]


class TestChainingColors:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield
  
  def test__chain_styles_colors(self, capsys, texts, colored):
    logger = TermStyle()

    logger.fg_blue().bg_yellow().strike(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["baseChainedColors"])

  def test_rgb_fg_bg(self, capsys, texts, colored):
    logger = TermStyle()

    logger.fg_rgb(61, 217, 187).bg_rgb(32, 87, 111, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["rgbChainedColors"])
  
  def test__multiple_fg_to_default_last(self, capsys, texts, colored):
    logger = TermStyle()

    logger.fg_red().fg_color("sky-blue").fg_rgb(61, 217, 187, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["foregroundPrecedence"])
  
  def test__multiple_bg_to_default_last(self, capsys, texts, colored):
    logger = TermStyle()

    logger.bg_red().bg_color("sky-blue").bg_rgb(61, 217, 187, text=texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["backgroundPrecedence"])
  
  def test__same_fg_color(self, capsys, texts, colored):
    logger = TermStyle()
    code = 1

    logger.fg_red().fg_red().fg_red(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["foreground"].format(code))
  
  def test__same_bg_color(self, capsys, texts, colored):
    logger = TermStyle()
    code = 1

    logger.bg_red().bg_red().bg_red(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["background"].format(code))

class TestLoggerWithSettings:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield
  
  def test__default_logging(self, capsys, texts, colored, mock_settings_config):
    logger = TermStyle(mock_settings_config)

    logger(texts["message"])
    captured = capsys.readouterr()

    assert captured.out == newline(colored["defaultSettings"])
