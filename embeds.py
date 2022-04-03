import discord
from discord.ext import commands
from discord.utils import get


cmd_help_embed = discord.Embed(title = 'Навигация по командам')

cmd_help_embed.add_field(name = '!start', value = 'Старт боты')
cmd_help_embed.add_field(name = '!clear', value = 'Очистка чата')
cmd_help_embed.add_field(name = '!mute', value = 'Ограничение чата')
cmd_help_embed.add_field(name = '!kick', value = 'удаление участника с сервера')
cmd_help_embed.add_field(name = '!ban', value = 'Ограничение доступа к серверу')
cmd_help_embed.add_field(name = '!я', value = 'Карточка участника')