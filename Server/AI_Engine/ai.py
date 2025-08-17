from dataclasses import asdict
from typing import Iterator, List
from numpy import float32, ndarray
from ollama import ChatResponse, chat
from db.chat_history_repository import ChatHistoryRepository
from db.models import ChatMessage
from collections.abc import Iterator
from faster_whisper import WhisperModel
from piper import AudioChunk, PiperVoice


class AI:
    def __init__(self):
        self.__speech_to_text_model = WhisperModel(
            "small", device="cpu", compute_type="int8"
        )  # could be "medium", "large-v3"

        self.__voice = PiperVoice.load(
            "AI_Engine/en_GB-northern_english_male-medium.onnx", use_cuda=False
        )

        self.__chat_history_repo = ChatHistoryRepository()
        self.__chat_history = self.__chat_history_repo.GetChatHistory()
        self.__chat_history_to_add: List[ChatMessage] = []
        self.__saving_chat_history = False

    def __transcribe(self, audio_np: ndarray[float32]) -> str:
        segments, info = self.__speech_to_text_model.transcribe(
            audio_np, beam_size=5, language="en", vad_filter=True
        )

        text = " ".join([seg.text for seg in segments])

        return text

    def __stream_ai_response(self, prompt: str) -> Iterator[ChatResponse]:
        message = ChatMessage("user", prompt)
        self.__chat_history.append(message)
        self.__chat_history_to_add.append(message)
        chat_history_dicts = [asdict(msg) for msg in self.__chat_history]
        stream = chat(
            model="phi3:mini",
            messages=chat_history_dicts,
            stream=True,
        )

        return stream

    def __stream_ai_response_audio(
        self, stream: Iterator[ChatResponse]
    ) -> Iterator[AudioChunk]:
        sentence = ""
        total_output = ""
        break_points = [".", "!", "?", ",", "-"]
        for chunk in stream:
            text = chunk["message"]["content"]
            sentence += text
            total_output += text
            break_point = any(bp in text for bp in break_points)
            if break_point:
                audio_chunks = self.__voice.synthesize(sentence)
                for chunk in audio_chunks:
                    yield chunk
                sentence = ""

        if sentence:
            audio_chunks = self.__voice.synthesize(sentence)
            for chunk in audio_chunks:
                yield chunk

        message = ChatMessage("assistant", total_output)
        self.__chat_history.append(message)
        self.__chat_history_to_add.append(message)

    def query_AI(self, audio_np: ndarray[float32]) -> Iterator[AudioChunk]:
        transcription = self.__transcribe(audio_np)

        if not transcription:
            return

        if self.__saving_chat_history:
            audio_chunks = self.__voice.synthesize(
                "Give me a second, I'm just trying to remember what we've talked about"
            )

            for chunk in audio_chunks:
                yield chunk
        else:
            response_stream = self.__stream_ai_response(transcription)
            audio_chunks = self.__stream_ai_response_audio(response_stream)
            for chunk in audio_chunks:
                yield chunk
            self.__chat_history_repo.AddChatHistory(self.__chat_history_to_add)
            self.__chat_history_to_add.clear()
            self.__saving_chat_history = False
