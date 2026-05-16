from adapters.cli import CliApp
from application.use_cases import CalculateAllCasesUseCase, CalculateSpecificCaseUseCase
from domain.services import ImportingCostCalculator


DOLLAR: float = 5.0
QUOTA: float = 1000.0


def main():
    calculator = ImportingCostCalculator(DOLLAR, QUOTA)

    all_cases_use_case = CalculateAllCasesUseCase(calculator)
    specific_case_use_case = CalculateSpecificCaseUseCase(calculator)

    app = CliApp(all_cases_use_case, specific_case_use_case)
    app.run()


if __name__ == "__main__":
    main()
