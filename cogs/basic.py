from discord_slash import cog_ext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_option, create_permission
from cogs import Base
from misc.addition import Roles, debug_server_id


class Basic(Base):

    @cog_ext.cog_slash(description='Отчистить сообщения', options=[
        create_option(name="amount", description="Кол-во удаленных сообщений (по умолчанию 50 - это максимум)",
                      option_type=4, required=False)
    ],
       permissions={
           debug_server_id: [
               create_permission(Roles.teacher, SlashCommandPermissionType.ROLE, True),
               create_permission(Roles.student, SlashCommandPermissionType.ROLE, False),
           ]
       })
    async def clear(self, ctx, amount: int = 50):
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Basic(bot))
