# ChatGPT Voice Assistant

Talk to an OpenAI model using your microphone. Speech is transcribed by OpenAI and the answer is spoken using OpenAI, Apple, or Google text-to-speech. API usage incurs charges.

## Install

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Git. Python 3.12 is recommended. On macOS, install PortAudio with `brew install portaudio`. On Debian/Ubuntu, install it with `sudo apt-get install portaudio19-dev python3-dev`. A microphone and audio output are required; grant your terminal microphone permission on macOS.

Then install the CLI from this repository:

```bash
curl -fsSL https://raw.githubusercontent.com/jakecyr/chatgpt-voice-assistant/master/install.sh | bash
```

The script installs the current repository version with `uv tool install`. Run `uv tool update-shell` and restart your shell if `gptassist` is not on your PATH. You can inspect `install.sh` before running it. The URL uses the published `master` branch, so changes in a local checkout must be published before this command includes them.

## Run

```bash
export OPENAI_API_KEY="your-api-key"
gptassist
```

Choose a microphone if prompted, then speak. Press Ctrl+C to stop. For options run `gptassist --help`. For example:

```bash
gptassist --open-ai-model gpt-6.1-terra --reasoning-effort low --max-tokens 1000 --tts openai
```

The default chat model is `gpt-6.1-terra` with low reasoning effort. The completion token limit includes reasoning tokens; raise it if replies are cut short. Model availability and supported reasoning levels depend on your OpenAI account and model. Transcription uses `whisper-1`; OpenAI speech uses `tts-1`. Google speech output uses network access; Apple speech requires macOS. `--lang` and `--tld` configure Google speech output. Never share your API key.

## From source

```bash
git clone https://github.com/jakecyr/chatgpt-voice-assistant.git
cd chatgpt-voice-assistant
uv sync --locked
uv run gptassist
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for tests and [CONTRIBUTING.md](CONTRIBUTING.md) for pull requests and releases.
