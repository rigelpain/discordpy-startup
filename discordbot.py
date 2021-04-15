from discord.ext import commands
import os
import traceback

# インストールした discord.py を読み込む
import discord
import datetime

import numpy as np
import random
import times

# 自分のBotのアクセストークンに置き換えてください
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()
pretime_dict = {}
duration_time = {}
duration_time_adjust = {}

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

@client.event
# ボイチャ状態の変化で発火
async def on_voice_state_update(member, before, after):
    print("ボイスチャンネルで変化がありました")

    if((before.self_mute is not after.self_mute) or (before.self_deaf is not after.self_deaf)):
        print("ボイスチャンネルでミュート設定の変更がありました")
        return

    elif(before.channel is not None and after.channel is not None):
        reply_text = member.roles[-2].name + " が " + after.channel.name + " に移動しました"
        await member.guild.system_channel.send(reply_text)

    elif(before.channel is None and len(after.channel.members) <= 1):
        pretime_dict[member.name] = datetime.datetime.now()
        # reply_text = member.roles[-2].name + " が " + after.channel.name + " に参加しました"
        # reply_text = member.mention + " が " + after.channel.name + " に参加しました"
        # await member.guild.system_channel.send(reply_text)

        embed = discord.Embed(title="通話開始", color=member.roles[-2].color)
        embed.add_field(name="なまえ",value=member.roles[-2].name)
        embed.add_field(name="チャンネル",value=after.channel.name)
        embed.set_thumbnail(url=member.avatar_url)
        await member.guild.system_channel.send(member.roles[0],embed=embed)

    elif(before.channel is None):
        pretime_dict[member.name] = datetime.datetime.now()
        reply_text = member.roles[-2].name + " が " + after.channel.name + " に参加しました"
        await member.guild.system_channel.send(reply_text)

#ボイチャ退室時の処理
    elif(after.channel is None and len(before.channel.members) == 0):
        duration_time[member.name] = pretime_dict[member.name] - datetime.datetime.now()
        duration_time_adjust[member.name] = int(duration_time[member.name].total_seconds()) * -1

        embed = discord.Embed(title="通話終了", color=member.roles[-2].color)
        embed.add_field(name="なまえ",value=member.roles[-2].name)
        embed.add_field(name="チャンネル",value=before.channel.name)
        embed.add_field(name="通話時間",value=times.get_h_m_s((duration_time_adjust[member.name])))
        embed.set_thumbnail(url=member.avatar_url)
        await member.guild.system_channel.send(embed=embed)

        del duration_time[member.name]

    elif(after.channel is None):
        duration_time[member.name] = pretime_dict[member.name] - datetime.datetime.now()
        duration_time_adjust[member.name] = int(duration_time[member.name].total_seconds()) * -1
        reply_text = member.roles[-2].name + " が "+ before.channel.name + " から抜けました。\n通話時間：" + str(times.get_h_m_s((duration_time_adjust[member.name])))
        await member.guild.system_channel.send(reply_text)
    
        del duration_time[member.name]

@client.event
async def on_message(message):
    if message.content.startswith('!game'):
        game_name = np.array(["おえかきの森","Gartic Phone","BGA"])
        game_link = np.array(["https://casual.hange.jp/oekaki/","https://garticphone.com/ja/","https://boardgamearena.com/"])
        game_rand = random.randint(0,2)

        embed = discord.Embed(title=game_name[game_rand], description=game_link[game_rand], color=0x4fdbde)

        await message.channel.send(embed=embed)


# Botの起動とDiscordサーバーへの接続
bot.run(token)