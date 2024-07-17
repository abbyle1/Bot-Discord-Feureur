import discord
import random
from unidecode import unidecode

###################################################
###                  prérequis                  ###
###################################################

# Definit une variable intents qui contient les "intents" par defaut de la bibliotheque discord.
# Les intents sont des informations sur les donnees que vous voulez recevoir depuis le serveur Discord.
intents = discord.Intents.default()
# Cette ligne active l'intent pour les "guilds" (serveurs discord), ce qui signifie que le bot sera informé de tous les changements au sein du serveur.
intents.guilds = True
# Cette ligne active l'intent pour les "guild_messages" (messages de salon), 
# ce qui signifie que le bot sera informe de tous les messages dans les salons auxquels il a acces.
intents.guild_messages = True
# Cette ligne cree un objet "bot" pour se connecter a Discord en utilisant les intents définis dans la variable intents.
bot = discord.Client(intents=intents)

###################################################
###                   listes                    ###
###################################################

# Liste des mots autorises
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

###################################################
###                  fonctions                  ###
###################################################

def returned_message(str):
    '''
    Cette fonction renvoie une chaine de caracteres que le bot enverra dans le chat, personnalise en fonction du message passé en parametre
    Arguments :
        message (Any) : le message auquel on souhaite repondre
    Retourne :
        str (String) : une chaine de caracteres qui sera publié dans le chat par le bot
    '''
    # on retire les caracteres spéciaux (sauf ' ', '-' et ''')
    str = ''.join(letter for letter in str if (letter.isalnum() or letter == ' ' or letter == '-' or letter == '\''))
    # on transforme la string en liste de mot
    liste = str.split()
    for mot in liste:
        mot = ''.join(letter for letter in mot if letter.isalnum())
    # si "quoi" et "antifeur" sont détectés, 1 chance sur 2 de publier un gif triste
    if 'quoi' in liste and ('antifeur' in liste or 'anti-feur' in liste or ('anti' in liste and 'feur' in liste)):
        n = random.randint(0,7)
        if (n < 4):
            return exhausted_gif[n]
        else:
            return ''
    # si "antifeur" est détecté uniquement, on fait remarquer que c'est inutile
    elif 'quoi' not in liste and ('antifeur' in liste or 'anti-feur' in liste or ('anti' in liste and 'feur' in liste)):
        return "Pourquoi se protéger si l'on n'utilise même pas le q-word ? 🙄"
    # si "quoi" est détecté uniquement, on répond : un gif 1 fois sur 2 ou "feur"
    elif 'quoi' in liste:
        n = random.randint(0,7)
        if n in range(4):
            return tab_gif[n]
        else:
            return 'feur'
    # si un mot contenant la séquence "quoi" est détecté, le bot le fait remarquer
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
    print("liste des salons disponibles :\n[serveur] :\t[salon]")
    # on print la liste des salons où le bot peut envoyer et lire des messages :
    for guild in bot.guilds: # parcourt les serveurs ou le bot est intégré
        for channel in guild.text_channels: # parcourt les salons du serveur
            if channel.permissions_for(guild.me).read_messages:
                if channel.permissions_for(guild.me).send_messages:
                    print(f"{guild.name} :\t{channel.name}")

@bot.event
async def on_message(message):
    contenu = message.content
    contenu = contenu.lower()
    contenu = unidecode(contenu) # on enleve les accents
    channel = message.channel

    # pour eviter que le bot ne se reponde a lui-meme
    if message.author == bot.user:
        print("bot is author") # XXX suppr
        return

    # gerer la discussion privee avec le bot
    elif channel.type == discord.ChannelType.private:
        message_to_send = returned_message(contenu)
        if message_to_send != "":
            await channel.send(message_to_send)
            return # XXX suppr ?
    
    # gerer la discussion dans un serveur
    else:
        try: # TODO ajouter timeout ?
            message = await channel.fetch_message(channel.last_message_id) # on recup le dernier message du salon
            content = unidecode(message.content.lower())
            if message.author != bot.user: # XXX répétition de code
                message_to_send = returned_message(content)
                if message_to_send != "":
                    await channel.send(message_to_send)
        except:
            print(f"erreur détectée dans {channel.name}")

###################################################
###                  lancement                  ###
###################################################

bot.run("YOUR_API_KEY")