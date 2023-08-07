from glob import glob
from json import dump, load
from pathlib import Path
from shutil import rmtree
from typing import Any, List


def create_dir(dir_path: Path) -> None:
    if not dir_path.exists():
        dir_path.mkdir(parents=True)


def delete_dir(dir_path: Path) -> None:
    if dir_path.exists():
        rmtree(dir_path)


def delete_file(file_path: Path) -> None:
    if file_path.exists():
        file_path.unlink()


def search_files(path_regex: Path = Path("*")) -> List[Path]:
    return [Path(path) for path in glob(str(path_regex), recursive=True)]


def exists(path: Path) -> bool:
    return path.exists()


def read_file(file_path: Path) -> str:
    with open(file_path) as file:
        return file.read()


def write_file(file_path: Path, data: str = "") -> None:
    with open(file_path, "w") as file:
        file.write(data)


def read_json_file(file_path: Path, **kwargs: Any) -> dict:
    with open(file_path) as file:
        return load(file, **kwargs)


def write_json_file(file_path: Path, data: dict, indent=2, **kwargs: Any) -> None:
    with open(file_path, "w") as file:
        dump(data, file, indent=indent, **kwargs)
