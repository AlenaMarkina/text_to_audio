import os
from pathlib import Path
import sys

# Get relative filepath of a given file

file = sys.argv[1] if len(sys.argv) else None

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent  # /Users/alena/PycharmProjects/text_to_audio
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

print()
print(f'ROOT_DIR: {ROOT_DIR}')
print(f'STATIC_ROOT: {STATIC_ROOT}')


def get_file_path(start_folder_path, file_name) -> None:
    for root, dirs, files in os.walk(start_folder_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)

            print(f'\nfile path: {file_path}\n')
            print(f'relative path: {os.path.relpath(file_path, STATIC_ROOT)}\n')
            break


get_file_path(ROOT_DIR, file)
