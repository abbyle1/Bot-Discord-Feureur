import discord
import random
from unidecode import unidecode
from dotenv import load_dotenv
# from discord.ext import commands
# import os

###################################################
###                  prérequis                  ###
###################################################

# Definit une variable intents qui contient les "intents" par defaut de la bibliotheque discord.
# Les intents sont des informations sur les donnees que vous voulez recevoir depuis le serveur Discord.
intents = discord.Intents.default()
# Cette ligne active l'intent pour les "guilds" (serveurs), ce qui signifie que le bot sera informe de tous les changements au sein du serveur.
intents.guilds = True
# Cette ligne active l'intent pour les "guild_messages" (messages de salon), 
# ce qui signifie que le bot sera informe de tous les messages dans les salons auxquels il a acces.
intents.guild_messages = True
# Cette ligne cree un objet "bot" pour se connecter a Discord en utilisant les intents définis dans la variable intents.
bot = discord.Client(intents=intents)

###################################################
###                   listes                    ###
###################################################

# Liste de String contenant une liste de mots autorises
authorised_words = [
    'quoiqu',
    'quoique',
    'quoi que ce',
    'quoi que se',
    'piquoit',
    'pouquoi',
    'séquoia',
    'taquoir',
    'carquois',
    'claquoir',
    'dacquois',
    'iroquois',
    'manquoit',
    'marquoir',
    'narquois',
    'pourquoi',
    'quoi que',
    'séquoias',
    'taquoirs',
    'claquoirs',
    'iroquoise',
    'marquoirs',
    'narquoise',
    'turquoise',
    'iroquoises',
    'narquoises',
    'turquoises',
    'métaséquoia',
    'tu-sais-quoi',
    'narquoisement',
    'je-ne-sais-quoi'
]
# Liste de gifs repondant 'feur'
tab_gif = [
    "https://tenor.com/view/feur-gif-23547897",
    "https://tenor.com/view/feur-theobabac-quoi-gif-24294658",
    "https://tenor.com/view/feur-meme-gif-24407942",
    "https://tenor.com/view/multicort-feur-gif-23304150"
]
# Liste de 'exhausted gifs'
exhausted_gif = [
    "https://tenor.com/view/marex-tanking-gif-27301657",
    "https://tenor.com/view/sad-cat-sunakook-tired-exhausted-gif-24687868",
    "https://tenor.com/view/rick-and-morty-rick-sad-sitting-lonely-gif-25485281",
    "https://tenor.com/view/breaking-bad-gustavo-gif-26322938"
]
# List des 'feured'
# feured_list = []

###################################################
###                  fonctions                  ###
###################################################

def returned_message(str):
    '''
    Cette fonction renvoie une chaine de caracteres que le bot enverra dans le chat, personnalise en fonction du message passe en parametre
    Arguments :
        message (Any) : le message auquel on souhaite repondre
    Retourne :
        str (String) : une chaine de caracteres qui sera publie dans le chat par le bot
    '''
    # on retire les caracteres spéciaux (sauf ' ', '-' et ''')
    str = ''.join(letter for letter in str if (letter.isalnum() or letter == ' ' or letter == '-' or letter == '\''))
    # on transforme la string en liste
    liste = str.split()
    for mot in liste:
        mot = ''.join(letter for letter in mot if letter.isalnum())
    if 'quoi' in liste and ('antifeur' in liste or 'anti-feur' in liste or ('anti' in liste and 'feur' in liste)):
        n = random.randint(0,7)
        if (n < 4):
            return exhausted_gif[n]
        else:
            return ''
    elif 'quoi' not in liste and ('antifeur' in liste or 'anti-feur' in liste or ('anti' in liste and 'feur' in liste)):
        return "Pourquoi se protéger si l'on n'utilise même pas le q-word ? 🙄"
    elif 'quoi' in liste:
        n = random.randint(0,11)
        if n in range(4):
            return tab_gif[n]
        else:
            return 'feur'
    for word in authorised_words:
        if (word in liste):
            return "...👀"
    else:
        return ""

##################################################
### fonctions d'evenement lies au bot Discord  ###
##################################################

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("liste des salons disponibles :\n[serveur] : [salon]")
    for guild in bot.guilds: # parcourt les serveurs ou le bot est integre
        for channel in guild.text_channels: # parcourt les salons du serveur
            if channel.permissions_for(guild.me).read_messages: # on regarde ceux ou le bot peut lire les messages
                if channel.permissions_for(guild.me).send_messages: # on regarde ceux ou le bot peut envoyer des messages
                    print(f"{guild.name} : {channel.name}")

@bot.event
async def on_message(message):
    contenu = message.content

    # pour eviter que le bot ne se reponde a lui-meme
    if message.author == bot.user:
        return

    # gerer la discussion privee avec le bot
    elif message.channel.type == discord.ChannelType.private and message.author != bot.user:
        contenu = contenu.lower() # on enleve les maj
        contenu = unidecode(contenu) # on enleve les accents
        message_to_send = returned_message(contenu)
        if message_to_send != "":
            await message.channel.send(message_to_send)
            # feured_list.append(last_message.author)

    # gerer la discussion dans un serveur
    else:
        for guild in bot.guilds: # parcourt les serveurs ou le bot est integre
            for channel in guild.text_channels: # parcourt les salons du serveur
                if channel.permissions_for(guild.me).read_messages: # on regarde ceux ou le bot peut lire les messages
                    if channel.permissions_for(guild.me).send_messages: # on regarde ceux ou le bot peut envoyer des messages
                        try: # certains salons auront un message qui fera planter le code
                            last_message = await channel.fetch_message(channel.last_message_id) # on doit recup le dernier message du salon
                            last_message.content = unidecode(last_message.content.lower()) # enleve maj et accents
                            if last_message.author != bot.user:
                                message_to_send = returned_message(last_message.content)
                                if message_to_send != "":
                                    await channel.send(message_to_send)
                                    # feured_list.append(last_message.author)
                        except:
                            print(f"error detected in {channel.name} but program still running")


##################################################
### fonctions de commande lies au bot Discord  ###
##################################################

# bot = commands.Bot(command_prefix='/', intents=intents)
# @bot.command(name="feured")
# async def print_list(ctx): # ctx = context, pour recup les infos pratiques telles que : nom de user, channel, etc.
#     await ctx.send("les feured sont :\n" + '\n'.join(feured_list))

###################################################
###                  lancement                  ###
###################################################

load_dotenv()
# bot.run(os.environ['TOKEN'])
bot.run("MTA1MzIyOTI5ODIxMjk0MTg1NA.GsSEw6.Sv37CPEucQL3DPPsSgOCipaS7K9_QTunJAo_2s")