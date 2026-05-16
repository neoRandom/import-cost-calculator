from dataclasses import dataclass


DOLAR: float = 5.0
QUOTA: float = 1000.0


@dataclass
class PersonalImportingCase:
    value: float
    is_declaring: bool
    is_clean: bool


class ImportTaxCalculator:
    def __init__(self, dolar: float, quota: float):
        self.dolar = dolar
        self.quota = quota

    def dolar_to_reais(self, value: float) -> float:
        return value * self.dolar


    def calculate_traditional_import(self, value: float) -> float:
        return self.dolar_to_reais(value) * 2


    def calculate_personal_import(self, value: float, is_declaring: bool, is_clean: bool) -> float:
        if is_declaring:
            return self.dolar_to_reais(value) + (self.dolar_to_reais(value - self.quota) * 0.5)
        elif is_clean:
            return self.dolar_to_reais(value)

        return self.dolar_to_reais(value) + self.dolar_to_reais(value - self.quota)


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
        total_cost = calculator.calculate_personal_import(value, is_declaring, is_clean)
        print(f"The total cost of the personal import is: R$ {total_cost:.2f}")
    else:
        print("Invalid import type. Please enter 'T' or 'P'.")
