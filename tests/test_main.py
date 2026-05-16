import sys
import pytest
from pytest import MonkeyPatch
import main


def test_load_config_cli_overrides_env(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "--dollar", "6.0", "--quota", "1500"])
    monkeypatch.setenv("DOLLAR_RATE", "7.0")
    monkeypatch.setenv("QUOTA_VALUE", "2000")

    assert main.load_config() == (6.0, 1500.0)


def test_load_config_uses_environment_when_cli_missing(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setenv("DOLLAR_RATE", "7.0")
    monkeypatch.setenv("QUOTA_VALUE", "2000")

    assert main.load_config() == (7.0, 2000.0)


def test_load_config_uses_defaults_when_no_cli_or_env(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.delenv("DOLLAR_RATE", raising=False)
    monkeypatch.delenv("QUOTA_VALUE", raising=False)

    assert main.load_config() == (main.DEFAULT_DOLLAR, main.DEFAULT_QUOTA)


def test_load_config_raises_value_error_for_invalid_env(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setenv("DOLLAR_RATE", "abc")
    monkeypatch.delenv("QUOTA_VALUE", raising=False)

    with pytest.raises(ValueError):
        main.load_config()


def test_load_config_exits_for_invalid_cli_value(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "--quota", "abc"])
    monkeypatch.delenv("DOLLAR_RATE", raising=False)
    monkeypatch.delenv("QUOTA_VALUE", raising=False)

    with pytest.raises(SystemExit):
        main.load_config()


def test_main_wires_dependencies_and_runs_app(monkeypatch: MonkeyPatch):
    class FakeCalculator:
        def __init__(self, dollar_rate: float, quota_value: float):
            self.dollar_rate = dollar_rate
            self.quota_value = quota_value

    class FakeAllCasesUseCase:
        def __init__(self, calculator: FakeCalculator):
            self.calculator = calculator

    class FakeSpecificCaseUseCase:
        def __init__(self, calculator: FakeCalculator):
            self.calculator = calculator

    class FakeApp:
        last_instance = None

        def __init__(self, all_cases_use_case: FakeAllCasesUseCase, specific_case_use_case: FakeSpecificCaseUseCase):
            self.all_cases_use_case = all_cases_use_case
            self.specific_case_use_case = specific_case_use_case
            self.run_called = False
            FakeApp.last_instance = self

        def run(self):
            self.run_called = True

    monkeypatch.setattr(main, "load_config", lambda: (6.0, 1500.0))
    monkeypatch.setattr(main, "ImportingCostCalculator", FakeCalculator)
    monkeypatch.setattr(main, "CalculateAllCasesUseCase", FakeAllCasesUseCase)
    monkeypatch.setattr(main, "CalculateSpecificCaseUseCase", FakeSpecificCaseUseCase)
    monkeypatch.setattr(main, "CliApp", FakeApp)

    main.main()

    assert FakeApp.last_instance is not None
    assert FakeApp.last_instance.run_called is True
    assert FakeApp.last_instance.all_cases_use_case.calculator.dollar_rate == 6.0
    assert FakeApp.last_instance.all_cases_use_case.calculator.quota_value == 1500.0
