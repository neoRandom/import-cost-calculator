# Test Plan

## Scope
Validate:
- configuration loading in main.py
- cost calculation rules in services.py
- use-case orchestration in use_cases.py
- CLI behavior in cli.py

## Test Levels
- **Unit tests**: domain and application logic
- **Integration tests**: config loading and use-case wiring
- **CLI tests**: user input/output flow

---

## 1) main.py — configuration loading

### Cases
| Test | Input | Expected |
|---|---|---|
| CLI overrides env and default | `--dollar 6.0 --quota 1500`, env set | CLI values used |
| Env used when CLI missing | no CLI args, env set | env values used |
| Default used when CLI and env missing | no CLI args, no env | defaults `5.0`, `1000.0` |
| Mixed sources | `--dollar 6.0`, env quota set | dollar from CLI, quota from env |
| Invalid env value | `DOLLAR_RATE=abc` | `ValueError` |
| Invalid CLI value | `--quota abc` | argparse error / exit |

### Notes
- Mock `os.getenv`
- Mock `argparse.ArgumentParser.parse_args`

---

## 2) services.py — business rules

### `to_reais`
| Test | Input | Expected |
|---|---|---|
| Converts dollars to reais | `10`, rate `5.0` | `50.0` |

### `calculate_traditional_importing_cost`
| Test | Input | Expected |
|---|---|---|
| Doubles converted value | `10`, rate `5.0` | `100.0` |

### `calculate_personal_importing_cost`
Use quota `1000.0`, rate `5.0`.

| Case | value | declaring | clean | Expected |
|---|---:|---|---|---:|
| Below quota, declaring | 900 | True | False | base only |
| Below quota, clean | 900 | False | True | base only |
| Below quota, not declaring, not clean | 900 | False | False | base only |
| Above quota, declaring | 1200 | True | False | base + 50% of excess |
| Above quota, clean, declaring false | 1200 | False | True | base only |
| Above quota, not declaring, not clean | 1200 | False | False | base + 100% of excess |
| Exactly at quota | 1000 | any | any | base only |

### Important rule checks
- Declaring always applies **50%** tax on amount above quota
- Not declaring and not clean applies **100%** tax on amount above quota
- Clean and not declaring applies **0%**
- Taxable amount must not go below zero

---

## 3) use_cases.py — application layer

### `CalculateAllCasesUseCase.execute`
| Test | Input | Expected |
|---|---|---|
| Returns all calculated variants | value `1200` | all fields populated correctly |

### `CalculateSpecificCaseUseCase.execute`
| Test | Input | Expected |
|---|---|---|
| Returns specific case result | `PersonalImportingCase(...)` | raw, traditional, and personal cost correct |
| Preserves case flags | any case | uses passed `is_declaring` and `is_clean` |

### Notes
- Mock `ImportingCostCalculator`
- Verify calls and return mapping

---

## 4) cli.py — interactive behavior

### Cases
| Test | Input sequence | Expected |
|---|---|---|
| Show all cases flow | `1`, value | calls all-cases use case and prints result |
| Specific case flow | `2`, value, yes, no | calls specific-case use case |
| Invalid choice | `3` | prints invalid choice message |
| Invalid float retry | `2`, `abc`, `100` | reprompts until valid |
| Yes/no parsing | `yes` / `no` | maps only `"yes"` to `True` |

### Notes
- Mock `input`
- Capture `print`
- Mock both use cases

---

## 5) Suggested priority

### Must-have
- `calculate_personal_importing_cost`
- `load_config`
- `CalculateAllCasesUseCase.execute`

### Nice-to-have
- CLI flow tests
- Invalid input tests
- Edge cases around exact quota

---

## 6) Acceptance criteria
- All domain rules pass
- Configuration precedence is correct:
  1. CLI arguments
  2. environment variables
  3. defaults
- CLI runs without crashing for valid input
- Invalid input is handled predictably
