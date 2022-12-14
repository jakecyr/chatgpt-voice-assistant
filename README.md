# OpenAI Vocal Chatbot

A simple interface to the OpenAI GPT-3 models with speech
to text for input and text to speech for the output from OpenAI.

## Setup

```bash
# create a new env
python -m venv env

pip install SpeechRecognition
brew install portaudio
brew link portaudio

# save the output of this command
brew --prefix portaudio
```

Run 
```bash
sudo vi $HOME/.pydistutils.cfg
```

and enter the following replacing values with the output saved above:

```text
[build_ext]
include_dirs=<PATH FROM STEP 3>/include/
library_dirs=<PATH FROM STEP 3>/lib/
```

Finally:
```bash
pip install pyaudio
pip install gtts
```

## Running

```
OPENAI_API_KEY=<OPEN API SECRET KEY HERE> python main.py
```

Start speaking and turn up your volume to hear the AI 
assistant respond.

Say the word "exit" to stop the application.

## References

[SpeechRecognition library docs](https://pypi.org/project/SpeechRecognition/1.2.3/)
