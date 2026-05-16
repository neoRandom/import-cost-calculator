from domain.models import PersonalImportingCase, TraditionalImportingCase


class ImportingCostCalculator:
    def __init__(self, dolar: float, quota: float):
        self.dolar = dolar
        self.quota = quota

    def dolar_to_reais(self, value: float) -> float:
        return value * self.dolar

    def calculate_traditional_importing_cost(self, case: TraditionalImportingCase) -> float:
        return self.dolar_to_reais(case.value) * 2

    def calculate_personal_importing_cost(self, case: PersonalImportingCase) -> float:
        if case.is_declaring:
            return self.dolar_to_reais(case.value) + (self.dolar_to_reais(case.value - self.quota) * 0.5)
        elif case.is_clean:
            return self.dolar_to_reais(case.value)

        return self.dolar_to_reais(case.value) + self.dolar_to_reais(case.value - self.quota)
