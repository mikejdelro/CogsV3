from .kudos import Kudos

def setup(bot):
    cog = Kudos(bot)
    bot.add_cog(cog)
