import os


def get_full_path(path: str) -> str:
    root_dir = os.path.dirname(os.path.abspath('run.py'))
    return os.path.join(*[root_dir] + path.lower().replace('\\', '/').split('/'))
