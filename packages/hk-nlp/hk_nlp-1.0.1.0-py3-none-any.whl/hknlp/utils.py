import os
import json
from glob import glob
from typing import Union, Tuple, List, Any


def load_json(path: str, encoding: str = 'utf-8') -> Union[Tuple, List]:
    with open(path, encoding=encoding) as r:
        return json.load(r)


def write_json(path: str, content: Any, encoding: str = "utf-8") -> None:
    with open(path, 'w', encoding=encoding) as w:
        json.dump(content, w)


def get_all_path(path: str, ext=None) -> List[str]:
    ext = ext if ext else ".*"
    ext = ext if ext.startswith(".") else ext
    glob(os.path.join(path, "**/*" + ext))


def chk_dir_and_mkdir(fullpath: str) -> None:
    dirs = [fullpath]
    while True:
        directory = os.path.dirname(dirs[0]) if not os.path.isdir(dirs[0]) else dirs[0]
        if directory == dirs[0] or not directory:
            break
        if directory:
            dirs.insert(0, directory)
    for dir in dirs[:-1]:
        if not os.path.isdir(dir):
            os.mkdir(dir)
        #sss
