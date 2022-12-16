import pyaudio
import speech_recognition as sr


class SpeechListener:

    def listen_for_speech(self):
        # obtain audio from the microphone
        r = sr.Recognizer()

        py_audio = pyaudio.PyAudio()
        default_input_name = py_audio.get_default_input_device_info()['name']

        # can change device_index to something other than 0 to change the input mic
        with sr.Microphone(device_index=0) as source:
            print(f"Listening for input with default mic '{default_input_name}'...")
            audio = r.listen(source)
            print("Received input.")

        return self._recognize_text_in_audio(audio)

    def _recognize_text_in_audio(self, audio):
        r = sr.Recognizer()

        try:
            return r.recognize_google(audio, show_all=False, with_confidence=False)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None
