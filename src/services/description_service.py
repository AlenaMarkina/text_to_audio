import os
import random
from pathlib import Path

import edge_tts
from edge_tts import VoicesManager


class BaseClass:
    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent  # '/Users/alena/PycharmProjects/text_to_audio'
    static_root = 'static'

    def __init__(self, country, city, landmark_name):
        self.country = country.lower()
        self.city = city.lower()
        self.landmark_name = '_'.join(landmark_name.split(' ')).lower()
        self.file_path = None
        self.file_extension = None
        self.file_name = None
        self.dir = None
        self.rel_path = None

    async def init(self):
        await self.set_filename()
        await self.set_filepath()
        await self.get_relpath()

    async def set_filename(self):
        self.file_name = f'{self.landmark_name}.{self.file_extension}'
        print(f'file_name: {self.file_name}')

    async def create_directories(self):
        dirs = os.path.join(BaseClass.root_dir, BaseClass.static_root, self.dir, self.country, self.city,
                            self.landmark_name)
        print(f'dirs: {dirs}')
        os.makedirs(dirs, exist_ok=True)

    async def set_filepath(self):
        self.file_path = os.path.join(BaseClass.root_dir, BaseClass.static_root, self.dir, self.country, self.city,
                                      self.landmark_name, self.file_name)
        print(f'file_path: {self.file_path}')

    async def get_relpath(self):
        self.rel_path = os.path.relpath(
            self.file_path,
            os.path.join(BaseClass.root_dir, BaseClass.static_root)
        )
        print(f'relpath: {self.rel_path}')


class Description(BaseClass):
    def __init__(self, country, city, landmark_name, landmark_description):
        super().__init__(country, city, landmark_name)
        self.landmark_description = landmark_description
        self.file_extension = 'txt'
        self.dir = 'text'

    async def clean_text(self):
        self.landmark_description = self.landmark_description.replace('\xa0', ' ').replace('\n', ' ')
        print(f'cleaned text:\n{self.landmark_description}\n')

    async def save_text(self):
        with open(self.file_path, 'w') as f:
            f.write(self.landmark_description)

    async def get_text(self):
        pass


class Audio(BaseClass):
    def __init__(self, country, city, landmark_name):
        super().__init__(country, city, landmark_name)
        self.dir = 'audio'
        self.language = 'ru'
        self.voice_gender = 'Male'
        self.file_extension = 'mp3'

    def set_audio_info(self): pass


class TextToAudioService:
    """
    Конвертация текста в аудио
    """

    def __init__(self, country, city, landmark_name, landmark_description):
        self.desc = Description(country, city, landmark_name, landmark_description)
        self.audio = Audio(country, city, landmark_name)

    async def prepare_to_tts(self):
        await self.desc.init()
        await self.audio.init()

        await self.desc.clean_text()
        await self.desc.create_directories()
        await self.desc.save_text()

        await self.audio.create_directories()

    async def text_to_audio(self):
        voices = await VoicesManager.create()
        voice = voices.find(Gender=self.audio.voice_gender, Language=self.audio.language)
        communicate = edge_tts.Communicate(self.desc.landmark_description, random.choice(voice)['Name'])
        await communicate.save(self.audio.file_path)

    async def worker(self):
        await self.prepare_to_tts()
        await self.text_to_audio()
