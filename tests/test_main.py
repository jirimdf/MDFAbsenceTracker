import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import main


def test_basic_calculation():
    assert main.calculate_absence(100, 10, 5, 25) == (10, 10.0, 15.0)


def test_remaining_hours_round_down():
    # 25 % of 99 hours is 24.75, so only 24 hours can be missed
    assert main.calculate_absence(99, 0, 0, 25)[0] == 24


def test_remaining_hours_never_negative():
    assert main.calculate_absence(100, 30, 0, 25)[0] == 0


def test_custom_limit():
    assert main.calculate_absence(200, 0, 0, 30)[0] == 60


@pytest.mark.parametrize("values", [(0, 0, 0), (100, -1, 0), (100, 0, -1)])
def test_invalid_input(values):
    with pytest.raises(ValueError):
        main.calculate_absence(*values, 25)


@pytest.mark.parametrize("content, expected", [("30", 30), ("abc", 25), ("150", 25)])
def test_load_max_percent(tmp_path, monkeypatch, content, expected):
    settings = tmp_path / "settings.txt"
    settings.write_text(content)
    monkeypatch.setattr(main, "SETTINGS_FILE", str(settings))
    assert main.load_max_percent() == expected


def test_saved_limit_is_used_after_restart(tmp_path, monkeypatch):
    settings = tmp_path / "settings.txt"
    settings.write_text("40")
    monkeypatch.setattr(main, "SETTINGS_FILE", str(settings))

    app = main.QApplication.instance() or main.QApplication([])
    window = main.MainWindow()
    window.total_hours_input.setText("100")
    window.absent_hours_input.setText("0")
    window.future_absent_hours_input.setText("0")
    window.calculate_percent()
    assert "can miss is: 40" in window.result_label.text()

    window.total_hours_input.setText("0")
    window.calculate_percent()
    assert window.result_label.text().startswith("Error")
    window.close()
