import os
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission


def get_full_path(path: str) -> str:
    ROOT_DIR: str = os.path.dirname(os.path.abspath('run.py'))
    if bool(os.environ.get('DEBUG', 0)):
        return os.path.join(*[ROOT_DIR] + path.lower().replace('\\', '/').split('/'))
    else:
        return os.path.join(*'home/QABot/'.split('/') + path.lower().replace('\\', '/').split('/'))


class Server:

    class Roles:
        student = 911196795210694687
        teacher = 911199136429248512

    id = 911196795210694686

    @staticmethod
    def get_cmd_permissions() -> dict:
        return {
            Server.id: [
                create_permission(Server.Roles.teacher, SlashCommandPermissionType.ROLE, True),
                create_permission(Server.Roles.student, SlashCommandPermissionType.ROLE, False),
            ]
        }

