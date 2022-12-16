import sys
import os
import signal
from computer_voice import ComputerVoice
from open_ai_client import OpenAIClient
from speech_listener import SpeechListener

openai_api_key = os.getenv("OPENAI_API_KEY")
previous_responses = []


def start_conversation():
    open_ai_client = OpenAIClient(openai_api_key)
    speech_listener = SpeechListener()
    computer_voice = ComputerVoice("temp.mp3")

    text = speech_listener.listen_for_speech()

    if text == "Exit" or text == "exit":
        sys.exit()

    if text is None or len(text) <= 1:
        start_conversation()

    response = open_ai_client.get_completion(text, previous_responses)
    previous_responses.append(response)

    response_text = response.get_computer_response()

    print(f"Open AI Response: {response_text}")

    with ComputerVoice() as computer_voice:
        computer_voice.speak(response_text)

    if not response.was_cut_short():
        print("Starting to listen again...")
        start_conversation()

    # If the response was cut short, let the user know they hit the max token limit
    with ComputerVoice() as computer_voice:
        computer_voice.speak("I apologize, but I ran out of tokens to finish my response.")


def signal_handler(sig, frame):
    print("Making sure temp files are cleaned up...")
    ComputerVoice.cleanup_temp_files()
    print('Closing conversation...')
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_conversation()
