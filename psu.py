#<--------------Imports Start-------------->
import requests
import discord
from discord.ext import commands
from discord.utils import get
import json
from datetime import date
import io
import asyncio
import threading
import os
#<--------------Imports End-------------->

#<--------------Prefix Start-------------->
async def get_pre(bot, message):
	with open("config.json") as f:
		pprefix = json.load(f)
		prefix = pprefix["prefix"]
	return prefix
#<--------------Prefix Stop-------------->
bot = commands.Bot(command_prefix=get_pre, self_bot=True)
bot.remove_command('help')
bot_config = json.loads(open("config.json", "r").read())
psubotid = bot_config["psu-bot-id"]
psubotserver = bot_config["psu-bot-server"]







@bot.command()
async def ob(ctx,*args):
	try:
		attachment_url = ctx.message.attachments[0].url
		script_to_obfuscate = str(requests.get(attachment_url).text)
	except:
		script_to_obfuscate = "none"

	if script_to_obfuscate == "none":
		embed = discord.Embed(title="Hey bitches its made by GameOverAgain#1875", description="", color=0xFF0000)
		embed.add_field(name="Error", value="`Error occured! {Please upload the .txt/.lua file.}`", inline=False)
		await ctx.send(embed=embed)
	else:
		server = bot.get_guild(psubotserver)
		member = server.get_member(psubotid)
		await member.send("!obfuscate")
		try:
				await bot.wait_for("message",timeout=60.0)
		except asyncio.TimeoutError:
			await ctx.send("Failed to obfuscate")
		else:
			f = io.StringIO(script_to_obfuscate)
			await member.send(file=discord.File(f, "script" + ".lua"))
			def check(file):
				return file.attachments != [] and file.author.id == psubotid
			try:
				fileforthing = await bot.wait_for("message",timeout=60.0,check=check)
			except asyncio.TimeoutError:
				await ctx.send("Failed to obfuscate")
			else:
				thingtoget = fileforthing.attachments[0].url
				readyfile = str(requests.get(thingtoget).text)
				f = io.StringIO(readyfile)
				await ctx.send(content="> `Obfuscation Completed`",file=discord.File(f, "script" + ".lua"))
				
			





def start():
	try:
		os.system("title Connecting to discord server")
		print("\n>> Connecting to discord servers...")

		with open("config.json") as f:
			token = json.load(f)
			bot.run(token["token"], bot=False)
	except Exception as e:
		print(f"\n>> Something went wrong, please check the error!\n>> Error: {e}")
		input()
threading.Thread(target=start, args=()).start()