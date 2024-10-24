import pytest

import pytermstyle.utils as utils

from .conftest import valid_rgbs, invalid_rgbs

class TestRGB:
  @pytest.mark.parametrize('rgb', valid_rgbs)
  def test__valid_rgb(self, rgb: list[str]):
    assert utils.is_rgb_valid(rgb) == True

  @pytest.mark.parametrize('rgb', invalid_rgbs)
  def test__invalid_rgb(self, rgb: list[str]):
    assert utils.is_rgb_valid(rgb) == False


class TestColor:
  @pytest.mark.parametrize('name', utils.extendedColors.keys())
  def test__valid_extended_color(self, name: str):
    assert utils.is_valid_color(name) == True

  @pytest.mark.parametrize('name', valid_rgbs[0])
  def test__valid_color_code(self, name: str):
    assert utils.is_valid_color(name) == True

  @pytest.mark.parametrize('name', invalid_rgbs[0])
  def test__invalid_color(self, name: str):
    assert utils.is_valid_color(name) == False


class Test4Bit:
  @pytest.mark.parametrize('name', utils.baseColors)
  def test__valid_4bit_foreground_code(self, name):
    expected_code = 30 + utils.baseColors.index(name)

    assert utils.get_4bit_color_code(name, "foreground") == str(expected_code)

  @pytest.mark.parametrize('name', utils.baseColors)
  def test__valid_4bit_background_code(self, name):
    expected_code = 40 + utils.baseColors.index(name)

    assert utils.get_4bit_color_code(name, "background") == str(expected_code)

  def test__invalid_4bit_code(self):
    with pytest.raises(ValueError) as ve_code:
      utils.get_4bit_color_code("unknown", "foreground") # type: ignore

    assert ve_code.type is ValueError
    assert str(ve_code.value) == "Color unknown does not have a supported 4-bit code"

    with pytest.raises(ValueError) as ve_mode:
      utils.get_4bit_color_code("red", "unknown") # type: ignore

    assert ve_mode.type is ValueError
    assert str(ve_mode.value) == "Color mode unknown is not supported"


class Test8Bit:
  @pytest.mark.parametrize('name', utils.extendedColors.keys())
  def test__valid_8bit_name(self, name: str):
    assert utils.get_8bit_color_code(name) == utils.extendedColors[name] # type: ignore

  @pytest.mark.parametrize('code', valid_rgbs[0])
  def test__valid_8bit_code(self, code: str):
    assert utils.get_8bit_color_code(code) == code

  @pytest.mark.parametrize('code', invalid_rgbs[0])
  def test__invalid_8bit_code(self, code: str):
    assert utils.get_8bit_color_code(code) == None
