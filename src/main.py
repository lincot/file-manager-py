from file_manager import FileManager
from colors import BLUE, RESET
from pathlib import Path
import toml


def main():
    config = toml.load('config.toml')
    working_dir = Path(config['working_dir']).expanduser().resolve()
    file_manager = FileManager(working_dir)
    while True:
        try:
            path = Path.cwd().relative_to(working_dir)
            print(f'{BLUE}{path}{RESET}\n> ', end='')
            file_manager.handle(input())
        except KeyboardInterrupt:
            print()
        except EOFError:
            print()
            exit()


if __name__ == '__main__':
    main()
