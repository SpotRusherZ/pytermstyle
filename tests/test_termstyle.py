import pytest

from pytermstyle.pytermstyle import TermStyle
from pytermstyle.definitions import textStyles, baseColors

from .conftest import newline

class TestNoSettings:
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
