from pathlib import Path
from os import listdir

dir_address: str = "/home/flu/Projects/blankDB/src/parser/default"
test_adress: str = "/home/flu/Projects/blankDB/test/parser/default"

dir_path: Path = Path(dir_address)
test_path: Path = Path(test_adress)

dir_files: list[str] = listdir(dir_path)

for file in dir_files:
    if file[0] != "_" and file[-3:] == ".py":
        new_path = test_path / f"test_{file}"
        new_path.touch()
