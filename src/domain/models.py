from dataclasses import dataclass


@dataclass(frozen=True)
class ImportingCase:
    value: float


@dataclass(frozen=True)
class TraditionalImportingCase(ImportingCase):
    pass


@dataclass(frozen=True)
class PersonalImportingCase(ImportingCase):
    is_declaring: bool
    is_clean: bool


@dataclass(frozen=True)
class CalculationResult:
    raw_cost: float
    traditional_importing_cost: float
    personal_declaring_cost: float
    personal_clean_cost: float
    personal_non_declaring_non_clean_cost: float
