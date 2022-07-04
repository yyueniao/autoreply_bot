from discord.ext import commands
from core.classes import Cog_Extension
import datetime
import logging
import traceback

class Events(Cog_Extension):

  


  def write_log(self, content):
    with open("log.txt","a",encoding='utf8') as log:
      log.write(f"\n{datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(hours=8),'%Y-%m-%d, %H:%M:%S')}: "+content)

  @commands.Cog.listener()
  async def on_ready(self):
    print(">>机器人已到场<<")
    self.write_log("bot loaded.")

  @commands.Cog.listener()
  async def on_error(self, event, *args, **kwargs):
    message = args[0] #Gets the message object
    logging.warning(traceback.format_exc()) #logs the error
    await self.bot.send_message(message.channel, "看起来你的这个命令触发了某个奇怪的bug，联系一下技术人员吧~") #send the message to the channel
  
def setup(bot):
    bot.add_cog(Events(bot))
