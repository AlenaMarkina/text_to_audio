import os.path
import sys
from pathlib import Path


IMG_EXTENSION = '.jpg'

dir_name = sys.argv[1] if len(sys.argv) else None
print(f'Renaming files in "{dir_name}" folder...')

# start_dir = '../../statics/images'
# start_dir = '.'  # запуск в терминале
root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
p = [path.as_posix() for path in root_dir.iterdir() if path.as_posix().endswith('/statics')][0]
p1 = [d for d in os.listdir(p) if d == 'images'][0]
start_dir = os.path.join(p, p1)

print('-----------------------------')
print(f'start_dir: {start_dir}')


def find_directory_and_files(start_folder_path, folder_name) -> tuple[str, list] | None:
    for root, dirs, files in os.walk(start_folder_path):
        if folder_name in dirs:
            full_path = os.path.abspath(os.path.join(root, folder_name))
            files = os.listdir(full_path)
            files = [f for f in files if f.endswith(IMG_EXTENSION)]
            print(f"Found given folder at: {full_path}")
            print(f'Found files at given folder: {files}')
            return full_path, files


def get_new_file_name(path, files) -> list[str]:
    prefix_name = '_'.join(path.split('/')[-2:])  # 'lisbon_st_georges_castle'

    new_list = [
        ''.join([prefix_name, str(num), IMG_EXTENSION])
        for num, file in enumerate(files, 1)
    ]
    print()
    print(new_list)
    return new_list


def main():
    # TODO: сделать проверку, что искомая папка находится в папке images, тк может быть папка
    #  с таким названием в другом месте. То есть сделать start_dir = images!!!!!!!
    try:
        full_path, files = find_directory_and_files(start_dir, dir_name)
        new_files_name = get_new_file_name(full_path, files)

        old_files_path = ['/'.join([full_path, f]) for f in files]
        new_files_path = ['/'.join([full_path, f]) for f in new_files_name]

        print()
        print(old_files_path)
        print()
        print(new_files_path)

        for i in zip(old_files_path, new_files_path):
            os.rename(i[0], i[1])
    except TypeError as err:
        print(err)


main()
