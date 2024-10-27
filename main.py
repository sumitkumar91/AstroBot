import os
import requests
from discord import Intents, Client
from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']

intents: Intents = Intents.default()
intents.message_content = True

PREFIXES = ['!', '?']

client: Client = commands.Bot(command_prefix=PREFIXES, intents=intents)

@client.event
async def on_ready() -> None:
  print(f'Logged in as {client.user}!')

@client.command(name = 'horoscope')
async def horoscope(ctx, sign: str, day: str):
  sign = sign.lower()
  day = day.lower()

  url = 'https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily'
  params = {
    'sign': 'aries',
    'day': 'Tomorrow'
  }
  headers = {
    'accept': 'application/json'
  }

  response = requests.get(url, params=params,     headers=headers)

  if response.status_code == 200:
    horoscope = response.json()  
    if ctx.prefix == '?':
      await ctx.author.send(f"Your horoscope for {sign.capitalize()} on {horoscope['data']['date']}:\n {horoscope['data']['horoscope_data']}")
      await ctx.send("I've sent your horoscope to your DM!")
    else:
      await ctx.send(f"{ctx.author.mention}, your horoscope for {sign.capitalize()} on {horoscope['data']['date']}:\n {horoscope['data']['horoscope_data']}")
  else:
    await ctx.send("Sorry, I couldn't fetch your horoscope.")

def main() -> None:
  client.run(token = TOKEN)

if __name__ == "__main__":
  main()


