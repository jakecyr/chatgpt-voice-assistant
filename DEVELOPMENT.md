# Development Setup

1. Install the package in editable mode with `pip install -e .`
2. Install all optional dev dependencies with `pip install '.[dev]'`

See the main [README.md file](./README.md) for general setup instructions.

## Testing

### Unit Tests

Run `pytest` to run all unit tests.

### Coverage Report

Get the coverage with:

```bash
coverage run --source chatgpt_voice_assistant -m pytest tests
```

View the coverage report:

```bash
coverage report --show-missing --fail-under=90
```
