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
