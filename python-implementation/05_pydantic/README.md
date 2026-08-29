# Learn Pydantic: Beginner to Advanced

A hands-on, run-it-yourself curriculum. Each file is self-contained, runnable,
and ends with an exercise. Work through them in numeric order.

## Setup

```bash
pip install "pydantic[email]" pydantic-settings
```

## Run any file

```bash
python 00_basic_models.py
```

## Curriculum

| # | File | Level | Topic |
|---|------|-------|-------|
| 00 | `00_basic_models.py` | Beginner | Defining models, instantiation, ValidationError basics |
| 01 | `01_field_types_and_constraints.py` | Beginner | Built-in types, `Field()` constraints (gt/lt/pattern/etc.) |
| 02 | `02_optional_defaults.py` | Beginner | Optional fields, defaults, `default_factory`, Union types |
| 03 | `03_nested_models.py` | Beginner→Intermediate | Models inside models, lists of models |
| 04 | `04_enums_and_literals.py` | Intermediate | `Enum` and `Literal` for fixed choice fields |
| 05 | `05_field_validators.py` | Intermediate | `@field_validator`, before/after mode, cross-field access via `info.data` |
| 06 | `06_model_validators.py` | Intermediate | `@model_validator`, whole-model and pre-parse validation |
| 07 | `07_computed_fields.py` | Intermediate | `@computed_field` vs plain `@property` |
| 08 | `08_serialization_and_aliases.py` | Intermediate | `model_dump()`, aliases, `@field_serializer` |
| 09 | `09_model_config.py` | Intermediate | `ConfigDict`: extra fields, frozen models, auto-trim |
| 10 | `10_strict_mode_and_coercion.py` | Advanced | Lax vs strict validation, type coercion pitfalls |
| 11 | `11_generic_models.py` | Advanced | Generic, reusable models with `TypeVar` |
| 12 | `12_custom_types_annotated.py` | Advanced | `Annotated` + `AfterValidator`, built-in constrained types, `EmailStr` |
| 13 | `13_settings_management.py` | Advanced | `pydantic-settings`, env vars, nested config |
| 14 | `14_error_handling.py` | Advanced | Structured error inspection, `TypeAdapter` |
| 15 | `15_advanced_patterns_and_mini_project.py` | Advanced (capstone) | Discriminated unions, recursive models, private attrs + mini project challenge |

## How to use this

1. Read the docstring at the top of each file first.
2. Run the file and read the output alongside the code.
3. Try the exercise at the bottom before moving on.
4. File 15 ends with a full mini-project challenge that combines everything.

## Notes

- Examples target **Pydantic v2** syntax (`field_validator`, `model_validator`,
  `ConfigDict`, `computed_field`) — not the older v1 API (`@validator`, `Config` class).
- `EmailStr` needs the optional `email-validator` dependency: `pip install pydantic[email]`.
- `pydantic-settings` is a separate package from core pydantic (split out in v2).
