import asyncio
import random
import os

import edge_tts
from edge_tts import VoicesManager
from playsound3 import playsound
from docx import Document


# TEXT = 'Палаццо Дориа Памфили расположился на одной из главных улиц итальянской столицы Виа дель Корсо недалеко от площади Венеции. Это один из самых больших и роскошных дворцов в центре Рима, который построен в XV веке. Palazzo Doria Pamphilj знаменит своей огромной площадью, ценнейшей коллекцией предметов искусства и запутанной семейной историей владельцев — старинного итальянского аристократического рода Дориа-Памфили.'
# OUTPUT_FILE = 'test.mp3'

# TODO: 1. Открыть текстовый файл
# TODO: 2. Конвертировать текст в аудио
# TODO: 3. Сохранить аудио в нужную папку


class TextConvertor:
    def __init__(self, text_path):
        self.__text_path: str = text_path
        self.__audio_path: str | None = None
        self.__voice: list | None = None
        self.__text: str | None = None

    @property
    def audio_path(self):
        return self.__audio_path

    async def init_voice(self):
        voices = await VoicesManager.create()
        self.__voice = voices.find(Gender='Male', Language='ru')
        print(self.__voice)

    async def read_text_file(self):
        ext = os.path.splitext(self.__text_path)[1].lower()
        print(2222, ext)

        if ext == '.docx':
            doc = Document(self.__text_path)
            self.__text = "\n".join([para.text for para in doc.paragraphs])
            # print(44444444444, self.__text)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    async def set_audiopath_from_textpath(self):
        self.__audio_path = self.__text_path.replace('text/', 'audio/').replace('docx', 'mp3')
        print(f'audio_path: {self.__audio_path}')

    async def convert_text_to_audio(self):
        communicate = edge_tts.Communicate(self.__text, random.choice(self.__voice)['Name'])
        await communicate.save(self.__audio_path)

    def play_audio(self):
        playsound(self.__audio_path)
