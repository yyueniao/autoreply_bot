from core.classes import Cog_Extension
from replit import db

class Db(Cog_Extension):
  
  async def reset(ctx):
    keys = db.keys()
    for key in keys:
      del db[key]
    db["number"] = "0"

def setup(bot):
    bot.add_cog(Db(bot))
