import pytest

from pytermstyle.settings import TermConfigException, TermSettings

@pytest.fixture
def invalid_config():
  return {
    "style": ["bold", "unknown", "underline"],
    "foreground": {
      "rgb": ["61", "256", "217"],
    },
    "background": {
      "color": "unknown"
    },
  }

def config_error(text):
  return f"Configuration errors: [{text}]"

class TestSettings:
  def test__has_settings(self, mock_settings_config):
    settings = TermSettings(mock_settings_config)

    assert settings.has_settings() == True
    assert settings.styles() == ["bold", "italic", "underline"]
    assert settings.rgb("foreground") == ["61", "217", "217"]
    assert settings.color("background") == "magenta"

  def test__empty_settings(self):
    settings = TermSettings()

    assert settings.has_settings() == False
    assert settings.styles() == []
    assert settings.rgb("foreground") is None
    assert settings.rgb("background") is None
    assert settings.color("foreground") is None
    assert settings.color("background") is None

  def test__add_settings(self):
    settings = TermSettings()
    assert repr(settings) == "{}"

    # Add style to settings
    settings.add_style("bold")
    assert settings.has_settings() == True
    assert repr(settings) == "{'style': ['bold']}"

    # Add more styles to settings
    settings.add_style("framed")
    assert settings.styles() == ["bold", "framed"]

    # Check for adding of color
    settings.add_color("light-green", "foreground")
    assert settings.color("foreground") == "light-green"

    # Overwrite existing color setting
    settings.add_color("orange", "foreground")
    assert settings.color("foreground") == "orange"

    # Add RGB value to settings
    settings.add_rgb(["21", "32", "255"], "background")
    assert settings.rgb("background") == ["21", "32", "255"]

    # Overwrite RGB setting with color
    settings.add_color("cyan", "background")
    assert settings.color("background") == "cyan"
    assert settings.rgb("background") is None

  def test__add_invalid_style(self, texts):
    settings = TermSettings()

    with pytest.raises(TermConfigException) as te:
      settings.add_style("unknown") # type: ignore

    assert te.type is TermConfigException
    assert str(te.value) == texts["invalidStyle"]
  
  def test__add_invalid_color(self, texts):
    settings = TermSettings()

    with pytest.raises(TermConfigException) as te:
      settings.add_color("unknown", "foreground") # type: ignore
    
    assert te.type is TermConfigException
    assert str(te.value) == texts["invalidColor"]
    assert settings.has_settings() == False

    with pytest.raises(ValueError) as te:
      settings.add_color("black", "unknown") # type: ignore
    
    assert te.type is ValueError
    assert str(te.value) == texts["invalidMode"]
  
  def test__add_invalid_rgb(self, texts):
    settings = TermSettings()

    with pytest.raises(TermConfigException) as te:
      settings.add_rgb(["1", "2"], "foreground")
    
    assert te.type is TermConfigException
    assert str(te.value) == texts["wrongRGBSize"]
    assert settings.has_settings() == False

    with pytest.raises(TermConfigException) as te:
      settings.add_rgb(["1", "2", "-4"], "foreground")
    
    assert te.type is TermConfigException
    assert str(te.value) == texts["wrongRGBFormat"]
    assert settings.has_settings() == False

    with pytest.raises(ValueError) as te:
      settings.add_rgb("black", "unknown") # type: ignore
    
    assert te.type is ValueError
    assert str(te.value) == texts["invalidMode"]

  def test__clear_settings(self, mock_settings_config):
    settings = TermSettings(mock_settings_config)
    assert settings.has_settings() == True

    settings.clear()
    assert settings.has_settings() == False

    # Make sure that input is not being mutated
    assert mock_settings_config is not None

  def test__invalid_style(self, texts):
    config = { "style": ["unknown"] }

    with pytest.raises(TermConfigException) as ste:
      TermSettings(config)

    assert ste.type is TermConfigException
    assert str(ste.value) == config_error(texts["invalidStyle"])

  def test__invalid_color(self, texts):
    config = {
      "foreground": {
        "color": "unknown"
      }
    }

    # Invalid color
    with pytest.raises(TermConfigException) as te:
      TermSettings(config)

    assert str(te.value) == config_error(texts["invalidColor"])

    # Both RGB and Color fields provided
    config["foreground"]["rgb"] = ["1", "1", "1"] # type: ignore

    with pytest.raises(TermConfigException) as te:
      TermSettings(config)

    assert str(te.value) == config_error(texts["mutuallyExclusive"])

    # RGB field wrong size
    config["foreground"] = { "rgb": ["255", "255"] } # type: ignore

    with pytest.raises(TermConfigException) as te:
      TermSettings(config)

    assert str(te.value) == config_error(texts["wrongRGBSize"])

    # RGB field with invalid values
    config["foreground"] = { "rgb": ["255", "255", "256"] } # type: ignore

    with pytest.raises(TermConfigException) as te:
      TermSettings(config)

    assert str(te.value) == config_error(texts["wrongRGBFormat"])

  def test__error_formatting(self, texts, invalid_config):
    with pytest.raises(TermConfigException) as te:
      TermSettings(invalid_config)

    expected_text = config_error(", ".join([
      texts["invalidStyle"],
      texts["wrongRGBFormat"],
      texts["invalidColor"]
    ]))

    assert str(te.value) == expected_text
