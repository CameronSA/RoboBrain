import numpy as np
import requests
import sounddevice as sd
from audio_input.record import get_mic_input

SERVER_URL = "http://127.0.0.1:8001/speech-to-speech"
SAMPLE_RATE = 22050
CHANNELS = 1

if __name__ == "__main__":
    with sd.OutputStream(
        samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16"
    ) as stream:
        while True:
            audio_bytes = get_mic_input()  # your microphone input
            with requests.post(SERVER_URL, data=audio_bytes, stream=True) as response:
                buffer = b""
                for chunk in response.iter_content(chunk_size=4096):
                    if not chunk:
                        continue
                    buffer += chunk
                    # Make sure buffer length is multiple of 2 bytes (int16)
                    while len(buffer) >= 2:
                        # Take all full samples from buffer
                        n_samples = len(buffer) // 2
                        audio_np = np.frombuffer(
                            buffer[: n_samples * 2], dtype=np.int16
                        )
                        stream.write(audio_np)
                        buffer = buffer[n_samples * 2 :]
