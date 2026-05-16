from domain.models import PersonalImportingCase, TraditionalImportingCase


class ImportingCostCalculator:
    def __init__(self, dollar: float, quota: float):
        self.dollar = dollar
        self.quota = quota

    def dollar_to_reais(self, value: float) -> float:
        return value * self.dollar

    def calculate_traditional_importing_cost(self, case: TraditionalImportingCase) -> float:
        return self.dollar_to_reais(case.value) * 2

    def calculate_personal_importing_cost(self, case: PersonalImportingCase) -> float:
        if case.is_declaring:
            return self.dollar_to_reais(case.value) + (self.dollar_to_reais(case.value - self.quota) * 0.5)
        elif case.is_clean:
            return self.dollar_to_reais(case.value)

        return self.dollar_to_reais(case.value) + self.dollar_to_reais(case.value - self.quota)
