from typing import Iterator, Optional, Dict
import string
import re

mapping = {letter: idx + 1 for idx, letter in enumerate(string.ascii_letters)}
DIR_COMMAND = "$ cd"
LS_COMMAND = "$ ls"
COMMAND = "$"
DIR = "dir"
ALL_SIZES = []


class Dir:
    def __init__(self,
                 name: str,
                 files: Optional[Dict[str, int]] = None,
                 folders: Optional[Dict[str, "Dir"]] = None,
                 parent: Optional["Dir"] = None,
                 level: int = 0
                 ):
        self.name = name
        self.files = files
        self.folders = folders
        self.parent = parent
        self.level = level

    def __str__(self):
        tabs = " " * 2 * self.level
        print(tabs, self.name, "folder", self.size())
        for k, v in self.files.items():
            print(tabs, k, v)
        for folder in self.folders.values():
            print(folder)
        return ''

    def size(self):
        sum_files = sum(value for value in self.files.values())
        sum_folders = sum(folder.size() for folder in self.folders.values())
        total_size = sum_files + sum_folders
        ALL_SIZES.append(total_size)
        return total_size


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _build_structure() -> Dir:
    root = None
    for line in _read_input_file():
        if DIR_COMMAND in line:
            new_dir = re.sub(f'\{DIR_COMMAND} ', '', line)
            if new_dir == "/":
                current_dir = Dir(name=new_dir, files={}, folders={}, level=0)
                root = current_dir
                continue
            elif new_dir == "..":
                current_dir = current_dir.parent
                continue
            else:
                current_dir = current_dir.folders[new_dir]
                continue

        if line == LS_COMMAND:
            continue

        if DIR in line:
            dir_name = re.sub(f'{DIR} ', '', line)
            folder = Dir(name=dir_name, parent=current_dir, files={}, folders={}, level=current_dir.level + 1)
            current_dir.folders[dir_name] = folder
            continue

        size, file_name = line.split()
        current_dir.files[file_name] = int(size)

    return root


def calculate_total():
    root = _build_structure()
    root.size()

    return sum(item for item in ALL_SIZES if item < 100_000)


def choose_directory_to_delete():
    root = _build_structure()
    total_size = root.size()

    to_delete = total_size - 40_000_000
    directories_big_enough = [item for item in ALL_SIZES if item > to_delete]

    return min(directories_big_enough)


if __name__ == "__main__":
    # print(calculate_total())
    print(choose_directory_to_delete())
