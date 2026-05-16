from typing import Generic, TypeVar

from src.domain.services import ImportingCostCalculator
from src.domain.models import CalculationResult, ImportingCase, PersonalImportingCase, TraditionalImportingCase


T = TypeVar("T", bound=ImportingCase)


class CalculateUseCase(Generic[T]):
    def execute(self, case: T) -> CalculationResult:
        raise NotImplementedError


class CalculateAllCasesUseCase(CalculateUseCase[TraditionalImportingCase]):
    def __init__(self, calculator: ImportingCostCalculator):
        self._calculator = calculator

    def execute(self, case: TraditionalImportingCase) -> CalculationResult:
        return CalculationResult(
            raw_cost=self._calculator.dollar_to_reais(case.value),
            traditional_importing_cost=self._calculator.calculate_traditional_importing_cost(case),
            personal_declaring_cost=self._calculator.calculate_personal_importing_cost(
                PersonalImportingCase(value=case.value, is_declaring=True, is_clean=False)
            ),
            personal_clean_cost=self._calculator.calculate_personal_importing_cost(
                PersonalImportingCase(value=case.value, is_declaring=False, is_clean=True)
            ),
            personal_non_declaring_non_clean_cost=self._calculator.calculate_personal_importing_cost(
                PersonalImportingCase(value=case.value, is_declaring=False, is_clean=False)
            ),
        )


class CalculateSpecificCaseUseCase(CalculateUseCase[PersonalImportingCase]):
    def __init__(self, calculator: ImportingCostCalculator):
        self._calculator = calculator

    def execute(self, case: PersonalImportingCase) -> CalculationResult:
        return CalculationResult(
            raw_cost=self._calculator.dollar_to_reais(case.value),
            traditional_importing_cost=self._calculator.calculate_traditional_importing_cost(TraditionalImportingCase(value=case.value)),
            personal_declaring_cost=self._calculator.calculate_personal_importing_cost(case),
            personal_clean_cost=0.0,
            personal_non_declaring_non_clean_cost=0.0,
        )
