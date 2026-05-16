
DOLAR: float = 5.0
QUOTA: float = 1000.0


def dolar_to_reais(value: float) -> float:
    return value * DOLAR


def calculate_traditional_import(value: float) -> float:
    return dolar_to_reais(value) * 2


def calculate_personal_import(value: float, is_declaring: bool, is_clean: bool) -> float:
    if is_declaring:
        return dolar_to_reais(value) + (dolar_to_reais(value - QUOTA) * 0.5)
    elif is_clean:
        return dolar_to_reais(value)

    return dolar_to_reais(value) + dolar_to_reais(value - QUOTA)

def main():
    value = float(input("Enter the value of the imported item in dollars: "))
    import_type = input("Enter the type of import ([T]raditional / [P]ersonal): ").upper()

    if import_type.startswith("T"):
        total_cost = calculate_traditional_import(value)
        print(f"The total cost of the traditional import is: R$ {total_cost:.2f}")
    elif import_type.startswith("P"):
        is_declaring = input("Are you declaring the import? ([Y]es / [N]o): ").upper().startswith("Y")
        is_clean = input("Are you clean (paid the taxes before)? ([Y]es / [N]o): ").upper().startswith("Y")
        total_cost = calculate_personal_import(value, is_declaring, is_clean)
        print(f"The total cost of the personal import is: R$ {total_cost:.2f}")
    else:
        print("Invalid import type. Please enter 'T' or 'P'.")
