from cogs import Base
from misc.addition import Server
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Basic(Base):

    @cog_ext.cog_slash(description='Отчистить сообщения', options=[
        create_option(name="amount", description="Кол-во удаленных сообщений (по умолчанию 50 - это максимум)",
                      option_type=4, required=False)], permissions=Server.get_cmd_permissions())
    async def clear(self, ctx: SlashContext, amount: int = 50):
        await ctx.channel.purge(limit=amount)
        await ctx.send('Отчистка чата выполнена', hidden=True)


def setup(bot):
    bot.add_cog(Basic(bot))
