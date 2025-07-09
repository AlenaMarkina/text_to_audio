import asyncio
import os
from pathlib import Path
import sys
import random

import edge_tts
from edge_tts import VoicesManager
from playsound3 import playsound
from docx import Document


file = sys.argv[1] if len(sys.argv) else None

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent  # /Users/alena/PycharmProjects/text_to_audio

print(1111, ROOT_DIR)


async def get_file_path(start_folder_path, file_name):
    for root, dirs, files in os.walk(start_folder_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)

            print(f'\nfile path:      {file_path}\n')
            return file_path


async def read_text_file(file_path) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    print(2222, ext)

    if ext == '.docx':
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        # print(44444, text)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return text


async def convert_to_audio(text, text_path):
    audio_path = text_path.replace('text/', 'audio/').replace('docx', 'wav')
    voices = await VoicesManager.create()
    voice = voices.find(Gender='Male', Language='ru')
    communicate = edge_tts.Communicate(text, random.choice(voice)['Name'])
    await communicate.save(audio_path)


async def main():
    file_path = await get_file_path(ROOT_DIR, file)
    text = await read_text_file(file_path)
    await convert_to_audio(text, file_path)


asyncio.run(main())
