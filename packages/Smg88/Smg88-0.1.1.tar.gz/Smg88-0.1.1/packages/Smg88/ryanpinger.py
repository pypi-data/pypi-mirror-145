import time
import discord

intents = discord.Intents.all()
#intents.message_content = True

client = discord.Client(intents=intents)
TOKEN = "OTU5MjYzNzU3NjczMDY2NTA2.YkZV_g.cuMAZc-BAK7lHWxkrZlWgT2LWeI"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

_MYID = 634212810275946496  # My id
_RYANID = 312130522283245570  # Ryans id

DebugChannel = None
TargetID = _RYANID
TargetMember = None
TargetChannel = None
STOPPINGING = False


@client.event
async def on_message(message):
    global DebugChannel
    global TargetChannel
    global TargetMember
    global TargetID
    global STOPPINGING
    if message.content.startswith("$$START"):
        STOPPINGING = False
        await message.channel.send(f"Started pinging :) you can now live in fear :thumbsup:")
        await DebugChannel.send(f"Started pinging :) :thumbsup:")
    if message.content.startswith("$$STOP"):
        STOPPINGING = True
        await message.channel.send(f"Stopped pinging :) you can now rest in peace :thumbsup:")
        await DebugChannel.send(f"Stopped pinging :) :thumbsdown:")
    if message.content.startswith("$$PING"):
      num = 0
      try:
        num = int(message.content[6:])
      except Exception as err:
        print(f"Error ocurred while parsing num of $$PINGs")
        await DebugChannel.send(f"Error ocurred while parsing num of $$PINGs")
        raise err
      if num <= 0:
        await DebugChannel.send("Number of pings left is <= 0, stopping !")
        return
      await PING()
      await message.channel.send(f"$$PING{num-1}")
    if message.author == client.user:
        return
    print(f"Message received: {message.content}")
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
    if message.content.startswith("$member"):
        DebugChannel = message.channel
        for member in client.get_all_members():
            await message.channel.send(f"Member id: {member.id}, member name: {member.name}")
            if member.id == TargetID:
                await message.channel.send(f"Found my pinging target!! TIME TO PING! {member.id} {member.name}")
                TargetMember = member
    if message.content.startswith("$PingMember"):
        await PING()


async def PING(delay: int = 5):
    if STOPPINGING:
        await DebugChannel.send("Pings have been disabled :)")
        time.sleep(delay)
        return "STOPPINGING flag on :)"
    try:
        TargetChannel = await TargetMember.create_dm()
        await TargetChannel.send(
            "Hey bro man if you are seeing this than yay it worked!\nRemember to pay me **$10** :) :thumbsup:\nIf you want to stop this ping, type '$$STOP' :) or '$$START' to enable")
        time.sleep(delay)
    except Exception as err:
        await DebugChannel.send(f"Could not ping person :( :( {err}")
        raise err  # Ensures that things like keyboard interrupt are handled :)

client.run(TOKEN)
