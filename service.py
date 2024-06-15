# coding=utf-8
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Generator

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.audio.transcription import Transcription
from pydub import AudioSegment

# Create directory to save transcriptions
TRANSCRIPTION_DIR = Path("transcriptions")
UPLOAD_DIR = Path("uploads")
os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)

load_dotenv("./.env")
OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

executor = ThreadPoolExecutor()
SEGMENT_LENGTH_MS = 5 * 60 * 1000
SEGMENT_LENGTH_S = 5 * 60


# use openai's whisper api to get transcription
async def transcribe_audio(audio_path: Path) -> Path:
    print("start to transcribe audio...")
    # segment audio
    print(f"reading audio from: {audio_path.absolute()}")
    audio = AudioSegment.from_file(audio_path)
    segments = [
        audio[i : i + SEGMENT_LENGTH_MS]
        for i in range(
            0,
            len(audio),
            SEGMENT_LENGTH_MS,
        )
    ]

    print("start to post segmented files to openai...")
    # post audio to openai
    transcriptions = await asyncio.gather(
        *[
            transcribe_segment(
                segment,
                idx,
                audio_path,
            )
            for idx, segment in enumerate(segments)
        ]
    )

    print("start to combine result and write into file...")
    # write result into txt file
    transcription_path = TRANSCRIPTION_DIR / f"{audio_path.name}.txt"
    for idx, transcription in enumerate(transcriptions):
        __write_transcription(
            response=transcription,
            transcription_path=transcription_path,
            segment_index=idx,
        )

    print("task finished...")
    return transcription_path


# Asynchronous function to transcribe a segment
async def transcribe_segment(segment: AudioSegment, segment_index: int, origin_path: Path) -> Transcription:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, __sync_transcribe_segment, segment, segment_index, origin_path)


# function to read and post audio data to OpenAI's API and get Whisper's format data
def __sync_transcribe_segment(segment: AudioSegment, segment_index: int, origin_path: Path) -> Transcription:
    segment_path = origin_path.parent / f"{origin_path.stem}-{segment_index}.mp3"
    segment.export(segment_path, format="mp3")
    print(f"segment file: {segment_path}")

    with open(segment_path, "rb") as f:
        response: Transcription = OPENAI_CLIENT.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
        f.close()

    return response


# function to write the transcription into a file
def __write_transcription(response: Transcription, transcription_path: Path, segment_index: int = 0) -> None:
    with open(transcription_path, "a+", encoding="UTF-8") as f:
        f.writelines(__format_whisper_result(response, segment_index))
        f.flush()


# read whisper's result and return format text
def __format_whisper_result(response: Transcription, segment_index: int = 0) -> Generator[str, Any, None]:
    response.to_dict()

    for segments in response.to_dict().get("segments", list()):
        start = segments['start'] + segment_index * SEGMENT_LENGTH_S
        end = segments['end'] + segment_index * SEGMENT_LENGTH_S
        text = segments['text']
        yield (f'{start//60:02.0f}:{start%60:02.0f} ~ {end//60:02.0f}:{end%60:02.0f}\t{text}\n')
