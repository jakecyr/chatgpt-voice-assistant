# Development Setup

1. Install the package in editable mode with `pip install -e .`
2. Install all optional dev dependencies with `pip install '.[dev]'`

## Linting

Sort all imports with:

```bash
isort --multi-line 3 --profile black --python-version 39 chatgpt_voice_assistant
```

Run `black chatgpt_voice_assistant/**/*.py` to automatically reformat all source files
based on the default configuration.

## Testing

### Unit Tests

Run `pytest` to run all unit tests.

### Coverage Report

Get the coverage with:

```bash
coverage run -m pytest tests
```

View the coverage report:

```bash
coverage report --fail-under=90 --include="chatgpt_voice_assistant/*"
```

