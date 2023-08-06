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
TargetID = _MYID
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
    if message.content.startswith("$$STOP"):
      STOPPINGING = True
      await message.channel.send(f"Stopped pinging :) you can now rest in peace :thumbsup:")
      await DebugChannel.send(f"Stopped pinging :) :thumbsdown:")
    if message.content.startswith("$$PING"):
        for i in range(int(message.content[6:])):
            await DebugChannel.send(f"Pinging {TargetMember.name} {int(message.content[6:])} times!")
            await PING()
            # time.sleep(1)
            time.sleep(60)


async def PING():
    if STOPPINGING:
        return "STOPPINGING flag on :)"
    try:
        TargetChannel = await TargetMember.create_dm()
        await TargetChannel.send(
            "Hey bro man if you are seeing this than yay it worked!\nRemember to pay me **$10** :) :thumbsup:\nIf you want to stop this ping, type '$$STOP' :)")
    except Exception as err:
        await DebugChannel.send(f"Could not ping person :( :( {err}")
        raise err  # Ensures that things like keyboard interrupt are handled :)

client.run(TOKEN)
