# Основная библиотека
import discord
from discord.ext import commands
from discord.utils import get

# Импорт сторонних библиотек
import io
import requests
import warnings
from PIL import Image, ImageFont, ImageDraw

# Импорт .py файлов из папки проекта
import config as cfg
import embeds as emb


warnings.filterwarnings("ignore", category=Warning)

bot = commands.Bot(command_prefix = '!')
bot.remove_command('help')

# Слова
hello_words = ['hello', 'hi', 'привет', 'хай', 'ky', 'ку', 'здарова', 'дароу', 'салам', 'privet']
answer_words = ['команды', 'команды сервера', 'что здесь делать']
bad_words = ['ютубер', 'геймер']


@bot.event
async def on_ready():
	print('Бот запущен!')

	await bot.change_presence(status = discord.Status.online, activity = discord.Game('Python'))

@bot.event
async def on_command_error(ctx, error):
	pass

@bot.event
async def on_member_join(member):
	channel = bot.get_channel(959528367718269012)
	role = discord.utils.get(member.guild.roles, id = 960126545509371934)

	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = f'``{member.name}`` присоеденился к серверу!',
												color = 0x0c0c0c))

@bot.event
async def on_message(message):
	# Чат-бот
	await bot.process_commands(message)
	
	msg = message.content.lower()

	if msg in hello_words:
		await message.channel.send('Привет! Чего желаешь?')
	elif msg in answer_words:
		await message.channel.send('Пропиши команду !help , чтобы получить список команд!')
	# Фильтрация чата :D
	elif msg in bad_words:
		await message.delete()
		await message.author.send(f'{message.author.name}, не надо такое писать!')




# Стартовая команда start
@bot.command()
async def start(ctx):
	user = ctx.message.author

	await ctx.send(f'Привет, {user.mention}!')

# Команда help для вывода навигации по командам
@bot.command()
async def help(ctx):
	await ctx.send(embed = emb.cmd_help_embed)

# Команда clear для очищения сообщений
@bot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int):
	await ctx.channel.purge(limit = amount)

# Команда mute для обеззвучивания участника
@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)

	mute_role = discord.utils.get(ctx.message.guild.role, name = 'mute')

	await message.add_roles(mute_role)
	await ctx.send(f'{member.mention} получает ограничение чата, за нарушение прав!')

# Команда kick для кика участника
@bot.command()
@commands.has_permissions(administrator = True)
async def Kick(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)

	await member.kick(reason = reason)
	await ctx.send(f'{member.mention} кикнут!')

# Команда ban для бана участника
@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)

	await member.ban(reason = reason)
	await ctx.send(f'{member.mention} забанен!')

# Сообщение в лс, отправителю команды
@bot.command()
async def send_a(ctx):
	await ctx.author.send('Hello World!')

# Сообщение в лс, любому участнику сервера
@bot.command()
async def send_m(ctx, member: discord.Member):
	await member.send(f'{member.name}, привет от {ctx.author.name}!')

@bot.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот присоеденился к каналу: {channel}')

@bot.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот отключился от каналу: {channel}')

@bot.command(aliases = ['я', 'обо_мне', 'моя_карточка', 'моя_карта']) # !обо_мне
async def user_card(ctx):
	await ctx.channel.purge(limit = 1)

	img = Image.new('RGBA', (305, 130), '#277ad9')
	url = str(ctx.author.avatar_url)

	response = requests.get(url, stream = True)
	response = Image.open(io.BytesIO(response.content))
	response = response.convert('RGBA')
	response = response.resize((100, 100), Image.ANTIALIAS)

	img.paste(response, (15, 15, 115, 115))

	idraw = ImageDraw.Draw(img)
	name = ctx.author.name # Kai41k
	tag = ctx.author.discriminator # 0476

	headline = ImageFont.truetype('arial.ttf', size = 20)
	undertext = ImageFont.truetype('arial.ttf', size = 12)

	idraw.text((145, 15), f'{name}#{tag}', font = headline)
	idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

	img.save('user_card.png')

	await ctx.send(file = discord.File(fp = 'user_card.png'))

# Обработка ошибок (try: except: )
@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')

	elif isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, у вас недостаточно прав, чтобы использовать эту команду!')





if __name__ == '__main__':
	bot.run(cfg.BOT_TOKEN)