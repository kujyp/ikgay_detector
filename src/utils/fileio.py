import json
import os

from src.utils import console


def make_parent_path_if_doesnt_exist(path):
    parent_path = os.path.dirname(path)
    if not path:
        return

    if not os.path.exists(parent_path):
        os.makedirs(parent_path)


def save_as_json(path, o):
    console.info(f"path=[{path}], o=[{o}]")
    make_parent_path_if_doesnt_exist(path)
    with open(path, 'w') as f:
        json.dump(o, f, indent=4, sort_keys=True, ensure_ascii=False)


def load_from_json_or_none(path):
    # console.info(f"path=[{path}]")
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except BaseException:
        return None
