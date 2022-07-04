from core.classes import Cog_Extension
from discord.ext import commands
import discord
import json

CHANNEL_ID = 883976818573590539
GUILD_ID = 879252094509518908

class TreeHole(Cog_Extension):
  contents = []
    

  @commands.command()
  async def treehole(self, ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.send(f'请在私聊处使用树洞功能哦~')
      return 0
    desc = "要发布新的匿名帖，请输入‘p’\n要回复别人的帖子，请输入‘r’\n要退出，请输入‘c’"
    embed = discord.Embed(title="匿名树洞",description=desc)
    await ctx.send(embed=embed)

    def check(m):
      if not m.channel == ctx.channel:
        return False
      if not m.author == ctx.message.author:
        return False
      if m.content in ['p', 'r', 'c']:
        return True
      else:
        return False

    msg = await self.bot.wait_for('message',check=check)
    if msg.content == 'p':
      await self.create_post(ctx)
    elif msg.content == 'r':
      await self.create_reply(ctx)
    else:
      await self.cancel(ctx)
  
  async def cancel(self, ctx):
    self.contents = []
    await ctx.send("已退出匿名树洞。")

    
  async def create_post(self, ctx, reply_id=None):
    if reply_id:
      reply_content = await self.get_content(reply_id)
      desc = f'回复{reply_content}\n\n'
    else:
      desc = " "
    embed = discord.Embed(title="匿名树洞 > 创建贴文", description = desc)
    text = "请在下面输入你想要发布的贴文，可以分多次输入。\n输入完成后，请回复‘done’\n如果想要退出，请回复‘cancel’。"
    embed.set_footer(text=text)
    await ctx.send(embed=embed)

    def check(m):
      if not m.channel == ctx.channel:
        return False
      if not m.author == ctx.message.author:
        return False
      if m.content in ['done', 'cancel']:
        return True
      else:
        self.contents.append(m.content)
        return False
        
    msg = await self.bot.wait_for("message",check=check)
    if msg.content == 'done':
      res = await self.confirm_post(ctx, reply_id)
      if not res:
        await self.create_post(ctx, reply_id)
    elif msg.content == 'cancel':
      await self.cancel(ctx)
    
  async def create_reply(self, ctx):
    last_id = self.get_last_id() 
    desc = f"请输入你想要回复的贴文id（目前最后一篇贴文是{last_id}）\n例：‘#21’"
    embed = discord.Embed(title="匿名树洞 > 选择回复贴文",description = desc)
    await ctx.send(embed=embed)


    def check(m):
      if not m.channel == ctx.channel:
        return False
      if not m.author == ctx.message.author:
        return False
      if self.is_id(m.content): 
        return True
      else:
        return False
    
    msg = await self.bot.wait_for("message", check=check)
    reply_content = await self.get_content(msg.content) 
    if not reply_content:
      await ctx.send("选择回复对象失败，估计有bug，联系一下技术人员吧~")
      await self.cancel(ctx)
    desc = f"确定要回复以下贴文？\n{reply_content}\n确认请输入‘Y’，否则输入‘N’重新选择回复对象。"
    embed = discord.Embed(title="匿名树洞 > 选择回复贴文",description = desc)
    await ctx.send(embed=embed)
    
    def confirm(m):
      if not m.channel == ctx.channel:
        return False
      if not m.author == ctx.message.author:
        return False
      if m.content in ['Y', 'N']:
        return True
      else:
        return False
    
    confirm_msg = await self.bot.wait_for("message", check=confirm)
    if confirm_msg.content == 'N':
      await self.create_reply(ctx)
    else:
      await self.create_post(ctx, msg.content)

  async def confirm_post(self, ctx, reply_id=None):
    if reply_id:
      reply_msg = await self.get_post_msg(reply_id)
      desc = f'*回复[{reply_id}]({reply_msg.jump_url})*\n\n'
    else:
      desc = ""
    post_content = '\n'.join(self.contents)
    post_id = self.get_new_id()     
    desc += f'**{post_id}:**\n```{post_content}```'
    embed = discord.Embed(title="匿名树洞 > 创建贴文 > 预览", description=desc)
    embed.set_footer(text="输入‘Y’立即发布，输入‘N’重新创建贴文")
    await ctx.send(embed=embed)

    def check(m):
      if not m.channel == ctx.channel:
        return False
      if not m.author == ctx.message.author:
        return False
      if m.content in ['Y', 'N']:
        return True
      else:
        return False
    
    reply_msg = await self.bot.wait_for("message",check=check)
    if reply_msg.content == 'N':
      await ctx.send("已取消发布，请重新输入。")
      self.contents = []
      return False
    else:
      post_embed = discord.Embed(title="匿名树洞", description = desc)
      post_embed.set_footer(text="请把悄悄话告诉本树洞~~")
      res = await self.send_post(post_embed, post_id)
      if res:
        await ctx.send("发布成功！")
      else:
        await ctx.send("发布失败，估计有bug，联系下技术人员吧！")
      self.contents = []
      return True
  
  async def get_content(self, post_id):
    msg = await self.get_post_msg(post_id)
    if not msg:
      return None
    content = msg.embeds[0].description
    return content

  async def send_post(self, embed, post_id):
    guild = self.bot.get_guild(GUILD_ID)
    channel = guild.get_channel(channel_id=CHANNEL_ID)
    if not channel:
      return False
    msg = await channel.send(embed=embed)
    self.save_item(post_id, msg.id)
    return True

  async def get_post_msg(self, post_id):
    msg_id = self.read_item(post_id)
    guild = self.bot.get_guild(GUILD_ID)
    channel = guild.get_channel(channel_id=CHANNEL_ID)
    if not channel:
      return None    
    return await channel.fetch_message(msg_id)




  
  #-------------------boss------------------

  #return something like '#13' if '#13' is the last post
  def get_last_id(self):
    with open('tree_hole.json','r') as jfile:
      tree_list = json.load(jfile)
    return '#' + str(len(tree_list))

  # check if target is an existing post id or not
  def is_id(self, target:str):
    with open('tree_hole.json','r') as jfile:
      tree_list = json.load(jfile)
    if not target.startswith('#'):
      return False
    if not target[1:].isdigit():
      return False
    index = int(target[1:])
    if index > 0 and index <= len(tree_list):
      return True

  #return something like '#13' if '#12' is the last post
  def get_new_id(self):
    with open("tree_hole.json","r") as jfile:
      tree_list = json.load(jfile)
    return '#' + str(len(tree_list)+1)

  # save to db. key is smt like '#13' and val is msg id
  def save_item(self, key:str, val:int):
    with open('tree_hole.json','r') as jfile:
      tree_list = json.load(jfile)
    tree_list.append(str(val))
    with open('tree_hole.json','w') as jfile:
      json.dump(tree_list, jfile)

  #read db by key (smt like '#13'),return msg id
  def read_item(self, key)->int:
    with open('tree_hole.json','r') as jfile:
      tree_list = json.load(jfile)
    return int(tree_list[int(key[1:])-1])

def setup(bot):
    bot.add_cog(TreeHole(bot))
