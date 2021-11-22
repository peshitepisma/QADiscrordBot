import os


def get_full_path(path: str) -> str:
    root_dir = os.path.dirname(os.path.abspath('run.py'))
    return os.path.join(*[root_dir] + path.lower().replace('\\', '/').split('/'))


class Roles:
    student = 911196795210694687
    teacher = 911199136429248512


debug_server_id = 911196795210694686
