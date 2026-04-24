import os
import aiohttp
import discord
from discord import app_commands

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def buscar_no_scraper(nome: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api:5000/scrape?jogo={nome}", timeout=aiohttp.ClientTimeout(total=60)) as response:
            return await response.json()


def montar_embed(dados: dict) -> discord.Embed:
    resultado = dados.get('resultado', {})
    nome_jogo = resultado.get('nome', 'N/A')
    nota = resultado.get('nota', 'N/A')

    embed = discord.Embed(
        title=f"🎮 {nome_jogo}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Metascore", value=nota, inline=True)
    return embed


@tree.command(name="jogo", description="Busca a nota de um jogo no Metacritic")
async def buscar_jogo(interaction: discord.Interaction, nome: str):
    await interaction.response.send_message(f"🔍 Buscando: {nome}...")

    try:
        dados = await buscar_no_scraper(nome)
        embed = montar_embed(dados)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Erro: {str(e)}")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot conectado como {client.user}")


client.run(TOKEN)

