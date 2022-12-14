

```bash
python -m venv env
pip install SpeechRecognition

brew install portaudio
brew link portaudio
brew --prefix portaudio
```

Run 
```bash
sudo nano $HOME/.pydistutils.cfg
```

and enter replacing values with the output of `brew --prefix portaudio`:

```
[build_ext]
include_dirs=<PATH FROM STEP 3>/include/
library_dirs=<PATH FROM STEP 3>/lib/
```

```bash
pip install pyaudio
```
