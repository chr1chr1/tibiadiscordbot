import asyncio
import datetime
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# STEP 0: LOAD TOKEN FROM SOMEWHERE ELSE
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)


# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty because intents were not enabled, probably")
        return

    prev = "0"
    if user_message[0] == '!':
        while 1:
            try:
                response: str = get_response(user_message[1:], prev)
                if response != '':
                    await message.channel.send(response)
            except Exception as e:
                print(e)
            now = datetime.datetime.now(datetime.timezone.utc)  # utc
            i = int(now.hour == 23)  # germany is utc + 1
            prev = (str(now.year) + '-' + "{:02d}".format(now.month+i) + '-' + "{:02d}".format(now.day) + 'T'
                    + "{:02d}".format((now.hour + 1) % 24) + ':' + "{:02d}".format(now.minute) + ':'
                    + "{:02d}".format(now.second) + 'Z')
            # await asyncio.sleep(60)  # world page updates every 5 minutes, but character page could update sooner

    else:
        try:
            response: str = get_response(user_message, prev)
            if response != '':
                await message.channel.send(response)
        except Exception as e:
            print(e)


# STEP 3: HANDLING BOT STARTUP
@client.event
async def on_ready() -> None:
    print('Thanita has logged in.')

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: {user_message}')
    await send_message(message, user_message)


# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()