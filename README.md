# Import Cost Calculator

A small CLI application for calculating Brazilian import costs.  
The project is structured to keep input handling, business rules, and domain logic separate so the calculator stays easy to test and evolve.

It calculates import costs using a dollar exchange rate and a quota value.  
It supports configuration through:

- command-line flags
- environment variables
- built-in defaults

This makes it practical for both direct use and automation.

> Disclaimer: This project used AI for guiding, learning, and controlled code generation. No decision were made without human analysis and intervention.

## Technologies

- Python 3.12+
- `pytest` for tests
- [`uv`](https://docs.astral.sh/uv/) for dependency and environment management
- [Nix](https://nixos.org/) flake support for reproducible development environments

## Installation

The project uses both Nix and uv. Nix provides an isolated environment for uv, while uv offers explicit dependency management and fast workflows.

### Using Nix

```zsh
nix develop
```

### Using `uv`

```zsh
uv sync
```

## Usage

Run the application from the project root:

```zsh
uv run -m src.main
```

### Configuration

The app reads configuration in this order:

1. **CLI arguments**
2. **environment variables**
3. **defaults**

#### CLI options

- `--dollar` — exchange rate
- `--quota` — quota value

Example:

```zsh
uv run -m src.main --dollar 6.0 --quota 1500
```

#### Environment variables

- `DOLLAR_RATE`
- `QUOTA_VALUE`

Example:

```zsh
export DOLLAR_RATE=7.0
export QUOTA_VALUE=2000
uv run -m src.main
```

#### Behavior

- CLI values override environment variables
- environment variables override defaults
- invalid CLI values should fail fast
- invalid environment values should raise a parsing error

## Features

- CLI-based cost calculation
- layered configuration resolution
- separation of domain logic from UI code
- testable application wiring
- fallback defaults for convenience

## Architecture / Engineering / Structure

The project's architecture is based on Hexagonal Architecture to keep business logic isolated from the cli, tests and tooling.

It's understood that, for the scope of the project, such architecture is overengineering, thus the main goal was learning more and getting used to with it.

Also, one of the main characteristics of HA is being lighter than Clean Architecture while maintaining business logic isolated, and applying Dependency Inversion and Single Responsibility principles, so it applies good practices with lower requirements, being a great choice for fast (but high-quality) development.

### Layers

- **`src/main.py`**  
  Application entrypoint and configuration wiring.

- **`src/adapters/cli.py`**  
  CLI-specific concerns such as argument parsing and presentation.

- **`src/application/use_cases.py`**  
  Orchestrates business workflows.

- **`src/domain/models.py`**  
  Core data structures.

- **`src/domain/services.py`**  
  Domain rules and calculations.

### Why this structure

- keeps the calculator logic independent of the CLI
- makes unit tests simpler and more reliable
- reduces coupling between input handling and cost rules
- allows each layer to evolve without rewriting the whole app

## Design Decisions

- **Source separation:** `src/` avoids accidental imports from the project root.
- **Use-case driven design:** application logic is placed behind use cases instead of being embedded in the CLI.
- **Explicit configuration precedence:** CLI > environment > defaults makes behavior predictable.
- **Fast failure on bad input:** invalid values are rejected early to prevent silent calculation errors.
- **Small, testable components:** each layer can be mocked or tested in isolation.

> Note: You can also read a bit of what I've learned [here](/docs/record.md).

## Folder Structure

```text
import_cost_calculator/
├── src/
│   ├── main.py
│   ├── adapters/
│   │   └── cli.py
│   ├── application/
│   │   └── use_cases.py
│   └── domain/
│       ├── models.py
│       └── services.py
├── tests/
│   └── test_main.py
├── docs/
│   └── test_plan.md
├── pyproject.toml
├── uv.lock
├── flake.nix
└── LICENSE
```

## Tests

Run the test suite with:

```zsh
uv run -m pytest
```

Or:

```zsh
uv run python -m pytest
```

From the project root.

### What the tests cover

- configuration loading
- precedence of CLI arguments over environment variables
- default fallback behavior
- error handling for invalid input
- application wiring and dependency construction

## License

This project is currently under an [MIT License](LICENSE).
