import os, requests, discord, tzsucks, time, calendar
from discord.ext import commands
from datetime import datetime

TOKEN = os.getenv("LEGIONBOTTOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="--", description="None", intents=intents)

@bot.event
async def on_ready():
    print('Ready')

@bot.command()
@commands.has_any_role("Honor Guard", "Tech Support")
async def status(ctx, status: str):
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(embed=discord.Embed(description="Status updated."))

@bot.command(aliases=['tz'])
async def timezone(ctx, inputZoneAbbreviation: str=None):
    if inputZoneAbbreviation == None:
        inputZoneAbbreviation = "UTC"
    
    result = tzsucks.GetTimeZone(inputZoneAbbreviation)
    await ctx.send(embed=discord.Embed(description=inputZoneAbbreviation + ": " + str(result.formatted.time())))

@bot.command(aliases=['tzc'])
async def timezoneconvert(ctx, inputTime: str,inputFromZoneAbbreviation: str, inputToZoneAbbreviation: str):
    timeToConvert = datetime.strptime(time.strftime("%d/%m/%y") + " " + inputTime, "%d/%m/%y %H:%M").timetuple()

    result = tzsucks.ConvertTimeZone(inputFromZoneAbbreviation, inputToZoneAbbreviation, int(calendar.timegm(timeToConvert)))

    replyEmbed = discord.Embed(title="Time Zone Conversion", description=inputFromZoneAbbreviation + " to " + inputToZoneAbbreviation)
    replyEmbed.add_field(name=inputFromZoneAbbreviation, value=datetime.fromtimestamp(time.mktime(timeToConvert)).time(),inline=True)
    replyEmbed.add_field(name=inputToZoneAbbreviation, value=str(result.formatted.time()),inline=True)

    await ctx.send(embed=replyEmbed)

bot.run(TOKEN)



