import discord.colour
import discord.embeds
import discord
from discord import app_commands
import requests
from discord.ext import commands


url  = "https://api.exchangerate-api.com/v4/latest/"
BOT_TOKEN = "<your token here>"
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.tree.command(name="exchange", description="View exchange rates for the given currencies")
async def exchangecurrency(interaction: discord.Interaction, amount:int, fromcur: str, tocur: str):
    try:
        request = requests.get(url=url+fromcur)
        ans = request.json()["rates"][tocur]
        embed = discord.embeds.Embed(title=f"Conversion from {fromcur} to {tocur}", 
                                     description=f"{amount} {fromcur} is equivalent to {ans} {tocur}",
                                     colour=0x2ecc71)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        print(e)
        await interaction.response.send_message("Error! One  of your entered currencies is most likely not supported!", ephemeral=True)


@bot.tree.command(name="currencies", description="List all supported currencies")
async def currencies(interaction: discord.Interaction):
    request = requests.get(url+"AED").json()
    text = "".join(i + "\n" for i in request["rates"])
    embed = discord.embeds.Embed(title="Supported currencies",
                                description=text)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="supported", description="See if a currency is supported, e.g. USD")
async def supported(interaction: discord.Interaction, currency: str):
    request = requests.get(url+"AED").json()
    if currency.strip().upper() in request["rates"]:
        await interaction.response.send_message(f"Yes, {currency} is supported!", ephemeral=True)
    else:
        await interaction.response.send_message(f"No, {currency} is not supported!", ephemeral=True)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

bot.run(BOT_TOKEN)
