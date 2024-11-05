import pytest
import logging

from pytermstyle.pytermstyle import create_logger
from pytermstyle.logger import TermStyleRecord, TermStyleFormatter, basicConfig

class TestRecord:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield
  
  def test__basic_record(self, mock_record):
    term_style = create_logger()
    record = TermStyleRecord(mock_record, term_style)

    assert record.colorStart == ""
    assert record.colorEnd == ""

  def test__no_color_record(self, mock_record, monkeypatch):
    monkeypatch.setenv('NO_COLOR', 'true')

    term_style = create_logger()
    record = TermStyleRecord(mock_record, term_style)

    assert record.colorStart == ""
    assert record.colorEnd == ""

  
  def test__record_settings(self, mock_record, mock_settings_config, texts):
    term_style = create_logger(mock_settings_config)
    record = TermStyleRecord(mock_record, term_style)

    assert record.colorStart == texts["startBaseFormat"]
    assert record.colorEnd == texts["endBaseFormat"]


class TestFormatter:
  @pytest.fixture(autouse=True)
  def setup_before_after(self, monkeypatch):
    monkeypatch.setenv('FORCE_COLOR', 'true')

    yield

  def test__default_settings(self, mock_record, colored, texts):
    formatter = TermStyleFormatter()
    mock_record.message = texts["message"]

    assert formatter.formatMessage(mock_record) == colored["defaultLoggerSettings"]
  
  def test__custom_settings(self, mock_record, colored, texts):
    formatter = TermStyleFormatter(settings={ "INFO": { "style": ["bold"] } })
    mock_record.message = texts["message"]

    assert formatter.formatMessage(mock_record) == colored["customLoggerSettings"]
  
  def test__custom_format(self, mock_record, colored, texts):
    formatter = TermStyleFormatter(
      "%(colorStart)s%(levelname)s:%(name)s:%(message)s%(colorEnd)s"
    )
    mock_record.message = texts["message"]

    assert formatter.formatMessage(mock_record) == colored["customFormatMessage"]
  
  def test__basic_config(self):
    basicConfig()

    assert type(logging.root.handlers[0].formatter) is TermStyleFormatter
