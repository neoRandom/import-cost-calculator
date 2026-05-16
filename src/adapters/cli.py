from src.application.use_cases import CalculateAllCasesUseCase, CalculateSpecificCaseUseCase
from src.domain.models import PersonalImportingCase, TraditionalImportingCase


class CliApp:
    def __init__(self, all_cases_use_case: CalculateAllCasesUseCase, specific_case_use_case: CalculateSpecificCaseUseCase):
        self._all_cases_use_case = all_cases_use_case
        self._specific_case_use_case = specific_case_use_case

    def _read_float(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid number. Try again.")

    def _read_yes_no(self, prompt: str) -> bool:
        return input(prompt).strip().lower().startswith("y")

    def run(self) -> None:
        print("Welcome to the Importing Cost Calculator!")
        print("1. Show all cases")
        print("2. Calculate for a specific case")

        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            value = self._read_float("Enter the value in dollars: ")
            result = self._all_cases_use_case.execute(TraditionalImportingCase(value=value))

            print(f"\nInitial Value: US$ {value:.2f}")
            print(f"Raw Cost: R$ {result.raw_cost:.2f}")
            print(f"Traditional Importing Cost: R$ {result.traditional_importing_cost:.2f}")
            print(f"Personal Importing Cost (Declaring): R$ {result.personal_declaring_cost:.2f}")
            print(f"Personal Importing Cost (Clean): R$ {result.personal_clean_cost:.2f}")
            print(f"Personal Importing Cost (Not Declaring & Not Clean): R$ {result.personal_non_declaring_non_clean_cost:.2f}")

        elif choice == "2":
            value = self._read_float("Enter the value in dollars: ")
            is_declaring = self._read_yes_no("Are you declaring the import? ([Y]es/no): ")
            is_clean = self._read_yes_no("Are you clean (paid the taxes before)? ([Y]es/no): ")

            case = PersonalImportingCase(
                value=value,
                is_declaring=is_declaring,
                is_clean=is_clean,
            )
            result = self._specific_case_use_case.execute(case)

            print(f"\nInitial Value: US$ {value:.2f}")
            print(f"Raw Cost: R$ {result.raw_cost:.2f}")
            print(f"Traditional Importing Cost: R$ {result.traditional_importing_cost:.2f}")
            print(f"Personal Importing Cost: R$ {result.personal_declaring_cost:.2f}")

        else:
            print("Invalid choice. Please select either 1 or 2.")
