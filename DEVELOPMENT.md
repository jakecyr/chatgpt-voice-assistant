# Development Setup

1. Install poetry ([official docs](https://python-poetry.org/docs/#installation) or with `pip install poetry`)
2. Install all dependencies with `poetry install`

See the main [README.md file](./README.md) for general setup instructions.

## Testing

### Unit Tests

Run `poetry run pytest` to run all unit tests.

### Coverage Report

Get the coverage with:

```bash
poetry run coverage run --source chatgpt_voice_assistant -m pytest tests
```

View the coverage report:

```bash
poetry run coverage report --show-missing --fail-under=90
```
