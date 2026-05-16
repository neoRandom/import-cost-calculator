from dataclasses import dataclass


@dataclass
class PersonalImportingCase:
    value: float
    is_declaring: bool
    is_clean: bool
