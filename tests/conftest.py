import pytest

@pytest.fixture
def texts():
  return {
    "invalidStyle": "Invalid styles: unknown",
    "invalidColor": "Color unknown is not supported.",
    "invalidMode": "Color mode unknown is not supported",
    "mutuallyExclusive": '"rgb" and "color" properties are mutually exclusive.',
    "wrongRGBSize": '"rgb" field must be a list in format: [r, g, b]',
    "wrongRGBFormat": "Provided values for RGB must be 0 <= color <= 255",
  }

valid_rgbs = [
  ['61', '217', '187'],
  ['1', '0', '230'],
  ['255', '255', '255']
]

invalid_rgbs = [
  ['unknown', '-10', '259'],
  ['-1', '5', '123'],
  ['61', '217', '256'],
  ['a', '32', '57'],
]

@pytest.fixture
def mock_settings_config():
  return {
    "style": [
      "bold",
      "italic",
      "underline",
    ],
    "foreground": {
      "rgb": ["61", "217", "217"],
    },
    "background": {
      "color": "magenta"
    },
  }
