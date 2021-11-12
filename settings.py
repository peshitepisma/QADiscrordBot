import os


class PathManager:

    root_dir = os.path.dirname(os.path.abspath('run.py'))

    @staticmethod
    def get_full_path(path: str) -> str:
        return os.path.join(*[PathManager.root_dir] + path.lower().replace('\\', '/').split('/'))