# Contributing

Open an issue to discuss substantial changes. Fork the repository, create a branch, and open a pull request against `master`. Do not commit credentials or API keys.

Install the prerequisites in [README.md](README.md), then run `uv sync --locked`. Run the checks in [DEVELOPMENT.md](DEVELOPMENT.md), and explain any tests you could not run in your PR. Audio and API changes should include mocked tests and, when possible, a real-device check.

Use a [Conventional Commits](https://www.conventionalcommits.org/) PR title, such as `feat(cli): add a voice option`, `fix: handle empty audio`, or `docs: clarify setup`. For breaking changes use `feat!: ...` or `feat(cli)!: ...` and describe migration steps. PRs are squash merged; keep the PR title as the squash commit title. An approval and passing required checks are needed before merging.

Release Please groups conventional commits into a release PR. `feat` triggers a minor version, `fix` and `perf` a patch, and a breaking change a major version. Other types normally do not trigger a release on their own. Review and merge the release PR to create a tag and GitHub release; releases are not automatically uploaded to PyPI.
