import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime
import respuestas
import opciones
import pytz

load_dotenv()

server_members = []


async def send_msg(message, user_message, is_private):
    try:
        resp = respuestas.handle_response(user_message)
        await message.author.send(resp) if is_private else await message.channel.send(resp)
    except Exception as e:
        print(e)

async def send_hour_msg(message, channel, num):
    try:
        msg = f'{message} {opciones.mensajes_con_actividad[num]}'
        await channel.send(msg)
    except Exception as e:
        print(e)

async def dont_send_hour_msg(member, channel, num):
    try:
        msg = f'{member} {opciones.mensajes_sin_actividad[num]}'
        await channel.send(msg)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = os.getenv('TOKEN')
    bot = discord.Client(intents = discord.Intents.all())

    @bot.event
    async def on_ready():
        change_status.start()
        print(f'loggeado como {bot.user}')
        global timers
        timers = datetime.now()

        for guild in bot.guilds:
            for channel in guild.text_channels:
                global general
                general = channel

        


    @tasks.loop(seconds=3600)
    async def change_status():
        
        channel = general
        await bot.change_presence(activity=discord.Game('online'))
        for member in channel.members:
            server_members.append(member.name)
            if member.name != bot.user.name: #no me interesa saber lo que hace el bot
                if (member.activity):
                        hora = datetime.now().hour 
                        
                        num = random.randint(0, 2) #para tirar respuestas en orden random

                        horario_local = member.activity.start.astimezone(pytz.timezone('America/Argentina/Buenos_Aires')) ##cambio la timezone del comienzo de la actividad
                        hora_start = horario_local.hour #a qué hora empezó a jugar

                        duracion_hora = hora - hora_start #hace cuánto está jugando
                        if(duracion_hora >= 1):
                            msg = (f'{member} está jugando a {member.activity} desde las {horario_local.hour}:{horario_local.minute} y hace {duracion_hora}hs!')
                            await send_hour_msg(msg, general, num)
                        else:
                            await dont_send_hour_msg(member, general, num)
                else:
                    pass

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return 
        
        channel = message.channel
        member = message.author

        if message.content[0] == '!':
            if (member.activity):
                hora = datetime.now().hour 

                num = random.randint(0, 2)

                horario_local = member.activity.start.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))
                hora_start = horario_local.hour

                duracion_hora = hora - hora_start

                print(f'{member} está jugando a {member.activity} desde las {horario_local.hour}:{horario_local.minute} y hace {duracion_hora}hs')
                
                if(duracion_hora > 2):
                    message = f'{member} está jugando a {member.activity} hace {duracion_hora}hs, '
                    await send_hour_msg(message, channel, num)
                elif(duracion_hora < 2):
                    await dont_send_hour_msg(member, channel, num)
            else:
                await channel.send(f'{member} está haciendo algo secreto')
        else:
            await send_msg(message, message.content, is_private=False)

    bot.run(TOKEN)