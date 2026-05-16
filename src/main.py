import argparse
import os

from src.adapters.cli import CliApp
from src.application.use_cases import CalculateAllCasesUseCase, CalculateSpecificCaseUseCase
from src.domain.services import ImportingCostCalculator


DEFAULT_DOLLAR: float = 5.0
DEFAULT_QUOTA: float = 1000.0
DOLLAR_ENV_VAR = "DOLLAR_RATE"
QUOTA_ENV_VAR = "QUOTA_VALUE"


def _load_float(cli_value: float | None, env_name: str, default_value: float) -> float:
    if cli_value is not None:
        return cli_value

    env_value = os.getenv(env_name)
    if env_value is not None:
        return float(env_value)

    return default_value


def load_config() -> tuple[float, float]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dollar", type=float, default=None)
    parser.add_argument("--quota", type=float, default=None)
    args = parser.parse_args()

    dollar = _load_float(args.dollar, DOLLAR_ENV_VAR, DEFAULT_DOLLAR)
    quota = _load_float(args.quota, QUOTA_ENV_VAR, DEFAULT_QUOTA)
    return dollar, quota


def main():
    dollar, quota = load_config()
    calculator = ImportingCostCalculator(dollar, quota)

    all_cases_use_case = CalculateAllCasesUseCase(calculator)
    specific_case_use_case = CalculateSpecificCaseUseCase(calculator)

    app = CliApp(all_cases_use_case, specific_case_use_case)
    app.run()


if __name__ == "__main__":
    main()
