from discord.ext import commands
import json
from core.classes import Cog_Extension
from discord.utils import get
import emoji
import random


with open("autoreply.json",'r',encoding='utf8') as jfile:
    autoreply_dict = json.load(jfile)
with open("autoemoji.json",'r',encoding='utf8') as jfile:
    autoemoji_list = json.load(jfile)


class Autoreply(Cog_Extension):
  THIS_BOT = 889453079223758859
  STOP_REPLY = "jfeijiJAIONOIEFWjoijc91298hf29oH9Q2H2O90n02f"
  TEST_CHANNEL = 886480461285716009
  emoji_pack = emoji

  @commands.Cog.listener()
  async def on_message(self, m):
    if not str(m.channel.id) in autoreply_dict[Autoreply.STOP_REPLY]:
      autoreply_dict[Autoreply.STOP_REPLY][str(m.channel.id)] = False
      with open("autoreply.json", 'w') as jfile:
        json.dump(autoreply_dict, jfile)
    if not (m.author.bot or autoreply_dict[Autoreply.STOP_REPLY][str(m.channel.id)]):
      dice = random.randint(1, 15)    
      if dice == 15:
        index = random.randint(0, len(autoemoji_list)-1)
        emoji_name = autoemoji_list[index]
        if emoji_name in self.bot.emojis:
            emoji = get(self.bot.emojis, name=emoji_name[1:-1])
        else:
            emoji = Autoreply.emoji_pack.emojize(emoji_name)
        await m.add_reaction(emoji)

      if m.content.endswith('nb'):
        await m.channel.send("我也觉得" + m.content)

      if m.content in autoreply_dict.keys():
        if autoreply_dict[m.content] == " ":
          del autoreply_dict[m.content]
          with open("autoreply.json", 'w') as jfile:
            json.dump(autoreply_dict, jfile)
        else:
          await m.channel.send(autoreply_dict[m.content])

  @commands.command()
  async def add_emoji(self, ctx, emoji=None):
    if not emoji:
      await ctx.send(f"请使用格式‘-add_emoji [emoji]’\n例：‘-add_emoji :+1:’")
      return 0
    if not emoji in autoemoji_list:
      autoemoji_list.append(emoji)
      await ctx.send(f"设定成功！")
    else:
      await ctx.send("此表情已存在。")
    with open("autoemoji.json","w") as f:
        json.dump(autoemoji_list, f)
    
  @commands.command()
  async def del_emoji(self, ctx, emoji=None):
    if not emoji:
      await ctx.send(f"请使用格式‘-del_emoji [emoji]’\n例：‘-del_emoji :+1:’")
      return 0
    for i in range(len(autoemoji_list)):
      if autoemoji_list[i] == emoji:
        del autoemoji_list[i]
        break
    await ctx.send(f"删除成功！")
    with open("autoemoji.json","w") as f:
        json.dump(autoemoji_list, f)


  @commands.command()
  async def stopreply(self, ctx, comm='on'):
    if comm == 'on':
      autoreply_dict[Autoreply.STOP_REPLY][str(ctx.message.channel.id)] = True
      await ctx.send("设定成功！此频道将不再自动回复。如果想重新开启自动回复，请回复‘-stopreply off’")
    elif comm == 'off':
      autoreply_dict[Autoreply.STOP_REPLY][str(ctx.message.channel.id)] = False
      await ctx.send("设定成功！此频道将开始自动回复。如果想关闭自动回复，请回复‘-stopreply on’")
    else:
      await ctx.send("请使用格式‘-stopreply [on/off]’\n例：‘-stopreply on’")
      return 0
    with open("autoreply.json", "w") as f:
      json.dump(autoreply_dict, f)


  @commands.command()
  async def autoreply(self, ctx, key=None, reply=None):
    if not (key and reply):
      await ctx.send("请使用格式‘-autoreply [key] [reply]’\n例：‘-autoreply 你好 你也好’")
      return 0
    if reply == ' ':
      del autoreply_dict[key]
      await ctx.send(f"已删除关键词‘{key}’")
    else:
      autoreply_dict[key] = reply
      await ctx.send(f"设定成功！试试看对我说‘{key}’吧~")
    with open("autoreply.json","w") as f:
        json.dump(autoreply_dict, f)

def setup(bot):
    bot.add_cog(Autoreply(bot))
