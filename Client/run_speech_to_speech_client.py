import requests

from audio_input.record import get_mic_input

server_url = "http://127.0.0.1:8001/speech-to-speech"

if __name__ == "__main__":
    while True:
        audio_bytes = get_mic_input()
        requests.post(server_url, data=audio_bytes)
