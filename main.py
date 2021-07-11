## Sam :)
## Created 10-07-21

## ---- tzsucks.py ----
# 
# Provides methods for accessing timezonedb's API.
#
# Requirements:
# - requests
# - timezonedb API key, stored as env var 'TIMEZONEDBKEY'
#
## --------------------


import os, requests, discord, time, calendar, sqlite3, shutil
from discord.ext import commands
from datetime import datetime
from PIL import Image, ImageFilter

from modules import tzsucks, scriptdict, profiledb


## ---------------------
### Bot Initialization
## ---------------------

TOKEN = os.getenv("LEGIONBOTTOKEN")
SCRIPTLOCATION = os.getenv("LEGIONBOTSCRIPTLOCATION")
PROFILEDBNAME = os.getenv("LEGIONBOTPROFILEDBNAME")
TZDB_KEY = os.getenv("TIMEZONEDBKEY")
IMAGE_DIRECTORY = 'images/'

db = sqlite3.connect(PROFILEDBNAME)
profiledb.InitializeProfileDatabase(db, False)

## Temporary
ProfileXDimension = 800;
ProfileYDimension = 400;

script = scriptdict.ScriptDict(SCRIPTLOCATION)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="--", description="None", intents=intents)

@bot.event
async def on_ready():
    print(script.Get('SYSTEM_ONREADY'))


## ---------------------
### Presence Commands
## ---------------------

@bot.command()
@commands.has_any_role("Honor Guard", "Tech Support")
async def status(ctx, *, status: str):
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(embed=discord.Embed(description=script.Get('COMMAND_STATUS_STATUSUPDATED')))


## ---------------------
### Timezone Commands
## ---------------------

## << timezone (zone) >>
## aliases: tzc
@bot.command(aliases=['tz'])
async def timezone(ctx, inputZoneAbbreviation: str=None):
    if inputZoneAbbreviation == None:
        inputZoneAbbreviation = "UTC"
    
    result = tzsucks.GetTimeZone(TZDB_KEY, inputZoneAbbreviation)
    await ctx.send(embed=discord.Embed(description=inputZoneAbbreviation + ": " + str(result.formatted.time())))

## << timezoneconvert [time, from, to] >>
## aliases: tzc
@bot.command(aliases=['tzc'])
async def timezoneconvert(ctx, inputTime: str,inputFromZoneAbbreviation: str, inputToZoneAbbreviation: str):
    timeToConvert = datetime.strptime(time.strftime("%d/%m/%y") + " " + inputTime, "%d/%m/%y %H:%M").timetuple()

    result = tzsucks.ConvertTimeZone(TZDB_KEY, inputFromZoneAbbreviation, inputToZoneAbbreviation, int(calendar.timegm(timeToConvert)))

    replyEmbed = discord.Embed(title="Time Zone Conversion", description=inputFromZoneAbbreviation + " to " + inputToZoneAbbreviation)
    replyEmbed.add_field(name=inputFromZoneAbbreviation, value=datetime.fromtimestamp(time.mktime(timeToConvert)).time(),inline=True)
    replyEmbed.add_field(name=inputToZoneAbbreviation, value=str(result.formatted.time()),inline=True)

    await ctx.send(embed=replyEmbed)


## ---------------------
### Profile Commands
## ---------------------

## << profile >>
## aliases: p
@bot.command(aliases=['p'])
async def profile(ctx, member: discord.Member=None):

    if member is None:
        member = ctx.author

    userProfile = profiledb.ReadUser(db, uid=member.id)

    if(userProfile == None):
        profiledb.CreateUser(db, member.id)
        userProfile = profiledb.ReadUser(db, uid=member.id)
    
    with open(IMAGE_DIRECTORY + userProfile.image, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

## << updateprofile >>
## aliases: up
@bot.command(aliases=['up'])
async def updateprofile(ctx, key: str, *, value: str=None):

    if value is None:
        value = "N/A"

    member = ctx.author

    userProfile = profiledb.ReadUser(db, uid=member.id)

    if(userProfile == None):
        profiledb.CreateUser(db, member.id)
        userProfile = profiledb.ReadUser(db, uid=member.id)
    
    if key == "pronouns":
        userProfile.pronouns = value
    elif key == "switch":
        userProfile.switch = value
    elif key == "psn" or key == "playstation":
        userProfile.psn = value
    elif key == "xbl" or key == "xbox":
        userProfile.xbl = value
    elif key == "battlenet" or key == "blizzard":
        userProfile.battlenet = value
    elif key == "image" or key == "background":
        
        if len(ctx.message.attachments) > 0:
            imageURL = ctx.message.attachments[0]
        else: imageURL = value

        fileExtension = imageURL.split(".")[-1]
        imageFilename = str(userProfile.discord_id) + "." + fileExtension

        r = requests.get(imageURL, stream=True)
        
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(IMAGE_DIRECTORY + imageFilename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        CropImage(IMAGE_DIRECTORY + imageFilename, ProfileXDimension, ProfileYDimension)
        BlurImage(IMAGE_DIRECTORY + imageFilename, 3)
        userProfile.image = imageFilename

    profiledb.UpdateUser(db, userProfile)

def CropImage(filename, w, h):
    im = Image.open(filename)
    width, height = im.size
    im1 = im.crop((0,0,800,400))
    im1.save(filename)

def BlurImage(filename, radius):
    im = Image.open(filename)
    im1 = im.filter(ImageFilter.GaussianBlur(radius=radius))
    im1.save(filename)


bot.run(TOKEN)