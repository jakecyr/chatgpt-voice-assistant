# OpenAI Vocal Chatbot

A simple interface to the OpenAI GPT-3 models with speech
to text for input and text to speech for the output from OpenAI.

## Setup

Optionally create a new Python environment and active it:

```bash
python3 -m venv env
source env/bin/activate
```

Install dependencies:

```bash
# Mac OSX
brew install portaudio
brew link portaudio

# save the output of this command
brew --prefix portaudio
```

Run 
```bash
sudo vi $HOME/.pydistutils.cfg
```

and paste the following text replacing the values with the output saved from above:

```text
[build_ext]
include_dirs=<PATH FROM STEP 3>/include/
library_dirs=<PATH FROM STEP 3>/lib/
```

Finally run:
```bash
pip install -r requirements.txt
```

## Running the Script

```bash
OPENAI_API_KEY=<OPEN API SECRET KEY HERE> python gpt3_assistant/main.py
```

Start speaking and turn up your volume to hear the AI 
assistant respond.

Say the word "exit" to stop the application.

## References

[SpeechRecognition library docs](https://pypi.org/project/SpeechRecognition/1.2.3/)


## Testing

The project has to be installed as a module first with:

```commandline
 pip install -e .
```

Then you can run `python -m pytest` to run all unit tests.
