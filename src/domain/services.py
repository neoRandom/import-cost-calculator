from domain.models import PersonalImportingCase, TraditionalImportingCase


class ImportingCostCalculator:
    def __init__(self, dollar_rate: float, quota_value: float):
        self.dollar_rate = dollar_rate
        self.quota_value = quota_value

    def dollar_to_reais(self, value: float) -> float:
        return value * self.dollar_rate

    def calculate_traditional_importing_cost(self, case: TraditionalImportingCase) -> float:
        return self.dollar_to_reais(case.value) * 2

    def calculate_personal_importing_cost(self, case: PersonalImportingCase) -> float:
        base_cost = self.dollar_to_reais(case.value)
        taxable_amount = max(0.0, case.value - self.quota_value)

        if case.is_declaring:
            tax_rate = 0.5
        elif case.is_clean:
            tax_rate = 0.0
        else:
            tax_rate = 1.0

        tax = self.dollar_to_reais(taxable_amount) * tax_rate
        return base_cost + tax
