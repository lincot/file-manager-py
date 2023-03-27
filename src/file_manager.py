from os import makedirs, rmdir, chdir
import os
from pathlib import Path
from sys import stderr
import sys
from colors import YELLOW, RESET
import shutil


class FileManager:
    def __init__(self, working_dir: Path):
        if not working_dir.exists():
            makedirs(working_dir)
        chdir(working_dir)
        self.working_dir = working_dir

    def handle(self, input: str):
        for (command, func) in [('mkfolder', self.make_folder),
                                ('rmfolder', self.remove_folder),
                                ('chfolder', self.change_folder),
                                ('mkfile', self.make_file),
                                ('wrfile', self.write_to_file),
                                ('shfile', self.show_file),
                                ('rmfile', self.remove_file),
                                ('cpfile', self.copy_file),
                                ('mvfile', self.move_file),
                                ('rnfile', self.rename_file)]:
            if input.startswith(command):
                try:
                    func(input[len(command + ' '):])
                except BaseException as err:
                    print(err, file=stderr)
                break
        else:
            print('unknown command', file=stderr)

    def check_path(self, path: str):
        path = Path(path).resolve()
        if not path.is_relative_to(self.working_dir):
            raise Exception("cannot exit working directory")
        return path

    def make_folder(self, path: str):
        makedirs(self.check_path(path))

    def remove_folder(self, path: str):
        rmdir(self.check_path(path))

    def change_folder(self, path: str):
        chdir(self.check_path(path))

    def make_file(self, path: str):
        open(self.check_path(path), 'x').close()

    def write_to_file(self, path: str):
        print(f'{YELLOW}write the text and then Ctrl+D:{RESET}')
        text = '\n'.join(sys.stdin.readlines())
        with open(self.check_path(path), 'a') as f:
            f.write(text)

    def show_file(self, path: str):
        with open(self.check_path(path), 'r') as f:
            print(f.read())

    def remove_file(self, path: str):
        self.check_path(path).unlink()

    def copy_file(self, args: str):
        [src, dst] = map(self.check_path, args.split(' '))
        shutil.copy(src, dst)

    def move_file(self, args: str):
        [src, dst] = map(self.check_path, args.split(' '))
        shutil.move(src, dst)

    def rename_file(self, args: str):
        [src, dst] = map(self.check_path, args.split(' '))
        os.rename(src, dst)
