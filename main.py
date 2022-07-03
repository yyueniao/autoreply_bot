import keep_alive
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix='-')
TEST_CHANNEL = 883976818573590539



  

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cmds.{extension}")
    await ctx.send(f"{extension} 更新完成")
    

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f"cmds.{filename[:-3]}")



if __name__ == "__main__":
  keep_alive.keep_alive()
  bot.run(TOKEN)
