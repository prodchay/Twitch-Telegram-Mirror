from twitchio.ext import commands
from dotenv import load_dotenv
import os
from telegram import Bot as TelegramBot
from datetime import datetime
import config
from asyncio import sleep as asyncsleep

load_dotenv()

print("=================\n" 
"Twitch => Twitch-Forwarder\n" 
"=================")

TWITCH_TOKEN = os.getenv('twitch_oauth_token')
TWITCH_NICK = config.twitch_nick
TWITCH_CHANNEL = config.twitch_channel
TWITCH_PREFIX = config.prefix

TELEGRAM_TOKEN = os.getenv('telegram_token')
TELEGRAM_CHAT_ID = os.getenv('telegram_chat_id')

telegram_bot = TelegramBot(token=TELEGRAM_TOKEN)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, prefix=TWITCH_PREFIX, initial_channels=[TWITCH_CHANNEL])
        self.start_time = datetime.now()

    async def event_ready(self):
        print(f"Connected as: {self.nick}")
        print(f"User ID {self.user_id}")

        channel = self.get_channel(TWITCH_CHANNEL)
        if channel:
            print(f"Connected to: {TWITCH_CHANNEL}.")
        else:
            print(f"Can't find the channel: {TWITCH_CHANNEL}.")

    async def event_message(self, message):
        if message.echo:
            return

        telegram_msg = f"{message.author.name}: {message.content}"
        await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=telegram_msg)
        await asyncsleep(0.3)

        await self.handle_commands(message)

    # own commands
    # X means the function has no parameters
    # Y means the function has optional parameters
    # Z means the function has required parameters

    @commands.command(name='test')
    async def test(self, ctx) -> None:
        """
        literally just a test command

        X
        """

        print("test")
        await ctx.send("test")

    @commands.command(name='uptime')
    async def uptime(self, ctx) -> None:
        """
        
        command used to check how long the bot has been running for 
        
        X
        """

        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        start_str = self.start_time.strftime("%A %d. %B %Y | %H:%M:%S")
        await ctx.send(f"Bot is running since: {start_str} | {hours}h {minutes}min {seconds}s")

if __name__ == "__main__":
    bot = Bot()
    bot.run()