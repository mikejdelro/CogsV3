from .badtouch import BadTouch

def setup(bot):
    cog = BadTouch(bot)
    bot.add_cog(cog)
