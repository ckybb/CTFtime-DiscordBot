import discord
from discord import app_commands
import json
import requests
import time
import datetime
import zoneinfo
import config

header = {"User-Agent": "Mozilla/5.0", "content-type": "application/json"}
dd = datetime.datetime
JST = zoneinfo.ZoneInfo('Asia/Tokyo')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
evecfg = False

@tree.command(name='eventcfg', description='eventコマンドのdescriptionを有効にするか設定します。')
async def set_eventcfg(interaction: discord.Interaction, value: bool):
    evecfg = value
    if evecfg:
        await interaction.response.send_message('descriptionを有効にしました。')
    else:
        await interaction.response.send_message('descriptionを無効にしました。')

@tree.command(name='event', description='現在から一週間後までで開催予定のCTF一覧を取得します。(最大10件)')
async def get_event(interaction: discord.Interaction):
    await interaction.response.defer()
    tstamp = int(time.time())
    res = requests.get(f'https://ctftime.org/api/v1/events/?limit=10&start={tstamp}&finish={tstamp+604800}', headers=header)
    if res.status_code != 200:
        await interaction.followup.send(f'取得できませんでした。status_code: {res.status_code}')
    else:
        data = res.json()
        n = len(data)
        embeds = []
        for i in range(n):
            starttime = dd.fromisoformat(data[i]["start"]).astimezone(JST)
            finishtime = dd.fromisoformat(data[i]["finish"]).astimezone(JST)
            if evecfg:
                embed = discord.Embed(title=data[i]["title"], color=0x00ff00, description=data[i]["description"][:2048], url=data[i]["url"])
            else:
                embed = discord.Embed(title=data[i]["title"], color=0x00ff00, url=data[i]["url"])
            embed.set_thumbnail(url=data[i]["logo"])
            embed.add_field(name='主催', value=data[i]["organizers"][0]["name"])
            if data[i]["location"] == "":
                embed.add_field(name='Location', value="On-Line")
            else:
                embed.add_field(name="Location", value=data[i]["location"])
            embed.add_field(name="形式", value=data[i]["format"])
            embed.add_field(name='開始時刻', value=starttime)
            embed.add_field(name='終了時刻', value=finishtime)
            embed.add_field(name='weight', value=data[i]["weight"])
            embed.add_field(name='URL', value=data[i]["url"])
            embed.add_field(name='URL(CTFtime)', value=data[i]["ctftime_url"])

            embeds.append(embed)

        await interaction.followup.send(f'{n}件開催予定です:\n', embeds=embeds)

@tree.command(name='description', description='CTF一覧の説明のみ表示します。')
async def get_description(interaction: discord.Interaction):
    await interaction.response.defer()
    tstamp = int(time.time())
    res = requests.get(f'https://ctftime.org/api/v1/events/?limit=10&start={tstamp}&finish={tstamp+604800}', headers=header)
    if res.status_code != 200:
        await interaction.followup.send(f'取得できませんでした。status_code: {res.status_code}')
    else:
        data = res.json()
        n = len(data)
        embeds = []
        for i in range(n):
            embed = discord.Embed(title=data[i]["title"], color=0x00ff00, description=data[i]["description"][:2048], url=data[i]["url"])
            embed.set_thumbnail(url=data[i]["logo"])
            embeds.append(embed)

        await interaction.followup.send(f'{n}件開催予定です:\n', embeds=embeds)


@tree.command(name='team', description='チームの情報を取得します。(RiST: 42506)')
async def get_team(interaction: discord.Interaction, id: int):
    await interaction.response.defer()
    res = requests.get(f'https://ctftime.org/api/v1/teams/{id}/', headers=header)
    if res.status_code != 200:
        await interaction.followup.send(f'取得できませんでした。status_code: {res.status_code}')
    else:
        data = res.json()
        year = str(dd.now().year)
        embed = discord.Embed(title=data["name"], color=0x00ff00, url=f'https://ctftime.org/team/{id}')
        embed.set_thumbnail(url=data["logo"])
        embed.add_field(name='Country', value=data["country"], inline=False)
        embed.add_field(name='ID', value=data["id"], inline=False)
        embed.add_field(name='世界順位', value=data["rating"][year]["rating_place"], inline=False)
        embed.add_field(name='国内順位', value=data["rating"][year]["country_place"], inline=False)
        embed.add_field(name='Rating', value=data["rating"][year]["rating_points"], inline=False)

        await interaction.followup.send(embed=embed)

@tree.command(name='rist', description='RiSTの情報を取得します。')
async def get_rist(interaction: discord.Interaction):
    await interaction.response.defer()
    res = requests.get(f'https://ctftime.org/api/v1/teams/42506/', headers=header)
    if res.status_code != 200:
        await interaction.followup.send(f'取得できませんでした。status_code: {res.status_code}')
    else:
        data = res.json()
        year = str(dd.now().year)
        embed = discord.Embed(title=data["name"], color=0x00ff00, url=f'https://ctftime.org/team/42506')
        embed.set_thumbnail(url=data["logo"])
        embed.add_field(name='Country', value=data["country"], inline=False)
        embed.add_field(name='ID', value=data["id"], inline=False)
        embed.add_field(name='世界順位', value=data["rating"][year]["rating_place"], inline=False)
        embed.add_field(name='国内順位', value=data["rating"][year]["country_place"], inline=False)
        embed.add_field(name='Rating', value=data["rating"][year]["rating_points"], inline=False)
        
        await interaction.followup.send(embed=embed)

@tree.command(name='shutdown', description='botを終了します。bot管理者のみ実行可能です。')
async def shutdown(interaction: discord.Interaction): 
    if interaction.user.id == int(config.ownerid):
        await interaction.response.send_message('Botを停止します。')
        print('received shutdown command.')
        await client.close()
    else:
        await interaction.response.send_message('bot管理者しか実行できません。')

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await tree.sync()

#async def on_message():


client.run(config.token)