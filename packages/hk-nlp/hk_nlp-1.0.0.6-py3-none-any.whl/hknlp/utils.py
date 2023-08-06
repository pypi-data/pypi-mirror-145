import os
import json
from typing import Union, Tuple, List, Any


def load_json(path: str, encoding: str = 'utf-8') -> Union[Tuple, List]:
    with open(path, encoding=encoding) as r:
        return json.load(r)


def write_json(path: str, content:Any, encoding: str = "utf-8") -> None:
    with open(path, 'w', encoding=encoding) as w:
        json.dump(content, w)


def get_all_path(path:str, ext=None) -> List[str]:
    all_path = []
    for d in os.listdir(path):
        sub = os.path.join(path, d)
        if os.path.isdir(sub):
            all_path += get_all_path(sub)
        else:
            if ext is None and os.path.splitext(sub)[-1] == ext:
                all_path.append(sub)
    return all_path


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