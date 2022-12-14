import sys
import speech_recognition as sr
import os
import openai
import signal
import gtts
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")
previous_responses = []


def start_conversation():
    audio = listen_for_audio()
    text = recognize_text_in_audio(audio)

    if text == "Exit" or text == "exit":
        sys.exit()

    if text is None or len(text) <= 1:
        start_conversation()

    response = get_response(text)
    previous_responses.append({"input": text, "response": response})
    print(f"Open AI Response: {response}")
    speak_response(response)

    print("Starting to listen again.")
    start_conversation()


def get_request_under_max_tokens(max_tokens, prompt):
    new_request = f"User:{prompt}\nAssistant: "
    request_header = ""

    for exchange in previous_responses:
        exchange_string = f"User: {exchange['input']}\nAssistant: {exchange['response']}"
        draft_request = f"{request_header}\n{exchange_string}\n{new_request}"

        if len(draft_request) > max_tokens:
            return f"{request_header}\n{new_request}"
        else:
            request_header += f"\n{exchange_string}"

    return f"{request_header}\n{new_request}"


# get response from openai GPT-3
def get_response(prompt):
    max_tokens = 100
    model = "text-davinci-003"
    request = get_request_under_max_tokens(max_tokens, prompt)

    completion = openai.Completion.create(
        model=model,
        prompt=request,
        max_tokens=max_tokens,
        temperature=0.7
    )

    first_choice = completion["choices"][0]["text"]
    first_choice = first_choice.replace("\n", " ")
    return first_choice.strip()


def speak_response(response):
    temp_mp3_filename = "temp.mp3"
    tts = gtts.gTTS(response)
    tts.save(temp_mp3_filename)
    full_mp3_path = os.path.join(os.getcwd(), temp_mp3_filename)
    subprocess.call(["afplay", full_mp3_path])
    os.remove(temp_mp3_filename)


def listen_for_audio():
    # obtain audio from the microphone
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for input...")
        audio = r.listen(source)
        print("Received input.")

    return audio


def recognize_text_in_audio(audio):
    r = sr.Recognizer()

    try:
        return r.recognize_google(audio, show_all=False, with_confidence=False)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def signal_handler(sig, frame):
    print('Closing conversation...')
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_conversation()
