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
        if case.is_declaring:
            return self.dollar_to_reais(case.value) + (self.dollar_to_reais(case.value - self.quota_value) * 0.5)
        elif case.is_clean:
            return self.dollar_to_reais(case.value)

        return self.dollar_to_reais(case.value) + self.dollar_to_reais(case.value - self.quota_value)
