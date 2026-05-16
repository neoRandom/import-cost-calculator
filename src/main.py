from application.use_cases import CalculateAllCasesUseCase, CalculateSpecificCaseUseCase
from domain.models import PersonalImportingCase, TraditionalImportingCase
from domain.services import ImportingCostCalculator


DOLAR: float = 5.0
QUOTA: float = 1000.0


def read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Try again.")


def read_yes_no(prompt: str) -> bool:
    return input(prompt).strip().lower().startswith("y")


def main():
    calculator = ImportingCostCalculator(DOLAR, QUOTA)
    all_cases_use_case = CalculateAllCasesUseCase(calculator)
    specific_case_use_case = CalculateSpecificCaseUseCase(calculator)

    print("Welcome to the Importing Cost Calculator!")
    print("1. Show all cases")
    print("2. Calculate for a specific case")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        value = read_float("Enter the value in dollars: ")
        result = all_cases_use_case.execute(TraditionalImportingCase(value=value))

        print(f"\nInitial Value: US$ {value:.2f}")
        print(f"Raw Cost: R$ {result.raw_cost:.2f}")
        print(f"Traditional Importing Cost: R$ {result.traditional_importing_cost:.2f}")
        print(f"Personal Importing Cost (Declaring): R$ {result.personal_declaring_cost:.2f}")
        print(f"Personal Importing Cost (Clean): R$ {result.personal_clean_cost:.2f}")
        print(f"Personal Importing Cost (Not Declaring & Not Clean): R$ {result.personal_non_declaring_non_clean_cost:.2f}")

    elif choice == "2":
        value = read_float("Enter the value in dollars: ")
        is_declaring = read_yes_no("Are you declaring the import? ([Y]es/no): ")
        is_clean = read_yes_no("Are you clean (paid the taxes before)? ([Y]es/no): ")

        case = PersonalImportingCase(
            value=value,
            is_declaring=is_declaring,
            is_clean=is_clean,
        )
        result = specific_case_use_case.execute(case)

        print(f"\nInitial Value: US$ {value:.2f}")
        print(f"Raw Cost: R$ {result.raw_cost:.2f}")
        print(f"Traditional Importing Cost: R$ {result.traditional_importing_cost:.2f}")
        print(f"Personal Importing Cost: R$ {result.personal_declaring_cost:.2f}")

    else:
        print("Invalid choice. Please select either 1 or 2.")


if __name__ == "__main__":
    main()
