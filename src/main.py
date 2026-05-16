from domain.models import PersonalImportingCase
from domain.services import ImportTaxCalculator


DOLAR: float = 5.0
QUOTA: float = 1000.0


def main():
    calculator = ImportTaxCalculator(DOLAR, QUOTA)

    value = float(input("Enter the value of the imported item in dollars: "))
    import_type = input("Enter the type of import ([T]raditional / [P]ersonal): ").upper()

    if import_type.startswith("T"):
        total_cost = calculator.calculate_traditional_import(value)
        print(f"The total cost of the traditional import is: R$ {total_cost:.2f}")
    elif import_type.startswith("P"):
        is_declaring = input("Are you declaring the import? ([Y]es / [N]o): ").upper().startswith("Y")
        is_clean = input("Are you clean (paid the taxes before)? ([Y]es / [N]o): ").upper().startswith("Y")

        case = PersonalImportingCase(value=value, is_declaring=is_declaring, is_clean=is_clean)
        total_cost = calculator.calculate_personal_import(case)
        print(f"The total cost of the personal import is: R$ {total_cost:.2f}")
    else:
        print("Invalid import type. Please enter 'T' or 'P'.")


if __name__ == "__main__":
    main()
