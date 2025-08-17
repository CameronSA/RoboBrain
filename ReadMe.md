# RoboBrain

A speech to speech system that leverages Whisper, Ollama and Piper to create a local conversational AI. It consists of a server and a client, where the intention is that the client is installed on a lightweight device such as a Raspberry Pi, and the server runs elsewhere to act as the main brain. Audio bytes are streamed to the client from the server to be played back with a device that is accesible to the client. This is a hobby project and not intended for production use.

# Usage

- Run `pip install -r requirements.txt` in each of the server and client directories.
- Ensure Ollama is running with the `phi3:mini` model installed
- Run `run_speech_to_speech_server.py`
- Run `run_speech_to_speech_client.py`
- Enjoy!
