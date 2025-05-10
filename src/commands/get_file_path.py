import os
from pathlib import Path
import sys


file = sys.argv[1] if len(sys.argv) else None

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
print(1111, ROOT_DIR)


def get_file_path(start_folder_path, file_name) -> None:
    for root, dirs, files in os.walk(start_folder_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)

            print(f'\nfile path:      {file_path}\n')
            break


get_file_path(ROOT_DIR, file)
