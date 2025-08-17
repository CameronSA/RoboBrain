from fastapi import FastAPI, Request
import numpy as np
import uvicorn

from AI_Engine.ai import AI

app = FastAPI()
ai = AI()


@app.post("/speech-to-speech")
async def speech_to_speech(request: Request):
    audio_bytes = await request.body()
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    ai.query_AI(audio_np)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
