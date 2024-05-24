# ChatGPT Voice Assistant

![GitHub Actions Build Status](https://github.com/jakecyr/openai-gpt3-chatbot/actions/workflows/test-application.yml/badge.svg)

A simple interface to the OpenAI ChatGPT model with speech to text for input and text to speech for the output.
chatgpt-voice-assistant uses OpenAI Whisper for speech transcription and OpenAI Speech Generation for TTS.

## Setup

### Mac Prerequisites

Install dependencies:

```bash
brew install portaudio
brew link portaudio
```

Update your pydistutils config file for portaudio usage by running the following:

```bash
echo "[build_ext]" >> $HOME/.pydistutils.cfg
echo "include_dirs="`brew --prefix portaudio`"/include/" >> $HOME/.pydistutils.cfg
echo "library_dirs="`brew --prefix portaudio`"/lib/" >> $HOME/.pydistutils.cfg
```

### Install from PyPI

Run the following to install the `chatgpt-assist` CLI application:

```bash
pip install chatgpt-voice-assistant
```

### Install from Source

1. Install poetry ([official docs](https://python-poetry.org/docs/#installation) or with `pip install poetry`)
2. Install all dependencies with `poetry install`

## Running the Script

Either set the `OPENAI_API_KEY` environment variable before running the script or pass in your secret key to the script like in the example below:

```bash
export OPENAI_API_KEY=<OPEN API SECRET KEY HERE>
gptassist

# OR

gptassist --open-ai-key=<OPEN API SECRET KEY HERE>
```

or if installed from source with poetry:

```bash
poetry run gptassist --open-ai-key=<OPEN API SECRET KEY HERE>
```

Start speaking and turn up your volume to hear the AI assistant respond.

Say the word "exit" or hit Ctrl+C in your terminal to stop the application.

### Options

Below is the help menu from the chatgpt-assist CLI detailing all available options:

```txt
-h, --help
    show this help message and exit

--log-level LOG_LEVEL
    Whether to print at the debug level or not.

--input-device-name INPUT_DEVICE_NAME
    The input device name.

--lang LANG
    The language to listen for when running speech to text (ex. en or fr).

--max-tokens MAX_TOKENS
    Max OpenAI completion tokens to use for text generation.

--tld TLD
    Top level domain (ex. com or com.au).

--safe-word SAFE_WORD
    Word to speak to exit the application.

--wake-word WAKE_WORD
    (Optional) Word to trigger a response.

--open-ai-key OPEN_AI_KEY
    Required. Open AI Secret Key (or set OPENAI_API_KEY environment variable)

--tts {apple,google,openai}
    Choose a text-to-speech engine.

--speech-rate SPEECH_RATE
    The rate at which to play speech. 1.0=normal
```

### Specifying an Output Language Accent

Specify both the `LANGUAGE` and `TOP_LEVEL_DOMAIN` vars to override the default English (United States)

```bash
gptassist --open-ai-key=<OPENAI_KEY> --lang=en --tld=com
```

#### Language Examples

- English (United States) _DEFAULT_
  - `LANGUAGE=en TOP_LEVEL_DOMAIN=com`
- English (Australia)
  - `LANGUAGE=en TOP_LEVEL_DOMAIN=com.au`
- English (India)
  - `LANGUAGE=en TOP_LEVEL_DOMAIN=co.in`
- French (France)
  - `LANGUAGE=fr TOP_LEVEL_DOMAIN=fr`

See Localized 'accents' section on gTTS docs for more information

## References

* [Speech Recognition library docs](https://pypi.org/project/SpeechRecognition/1.2.3)
* [Google Translate Text-to-Speech API (gTTS)](https://gtts.readthedocs.io/en/latest/module.html#)
