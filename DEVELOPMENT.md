# Development

Install uv and the PortAudio prerequisites described in the README, then run `uv sync --locked`.

```bash
uv run pytest
uv run coverage run --source=chatgpt_voice_assistant -m pytest
uv run coverage report --show-missing
uv run ruff check .
uv run ruff format --check .
```

Update dependencies with `uv lock --upgrade` and commit `uv.lock`. Tests mock external services and do not replace a live microphone, audio playback, or OpenAI API test.

## Release automation

Release Please needs a `RELEASE_PLEASE_TOKEN` Actions secret for an automation identity with repository contents and pull-request write access. That identity must also be allowed to create protected `v*` tags. A GitHub App or fine-grained token can be used; PRs created with the default `GITHUB_TOKEN` do not trigger the normal CI workflows. The release PR updates the package version, lockfile and changelog. Merge it after checks and review; the next workflow run creates the GitHub release and tag. Do not share credentials in an issue or PR.
