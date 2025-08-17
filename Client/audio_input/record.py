import sounddevice
import numpy as np

audio_buffer = bytearray()


def audio_callback(indata, frames, time, status):
    global audio_buffer
    audio_bytes = indata.tobytes()
    audio_buffer.extend(audio_bytes)


def get_mic_input():
    input("🎤 Press Enter to start recording...")
    audio_buffer.clear()

    with sounddevice.InputStream(
        samplerate=16_000, channels=1, dtype="int16", callback=audio_callback
    ):
        input("🎤 Recording. Press Enter to stop...")

    print("Recording stopped")
    return audio_buffer
