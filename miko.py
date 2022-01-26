import discord

import random
import requests
from discord.ext import tasks
from keep_alive import keep_alive

client = discord.Client()

isActive = True

game_list = [
    "Ghost of Tsushima",
    "Animal Crossing: New Horizons",
    "Monster Hunter: World",
    "Yakuza 0",
    "VALORANT",
    "League of Legends",
]

"""
insults_keywords = [
    'crazy',
    'funny',
    'poop',
    'huge',
    'dumb',
    'stupid',
    'stoopid',
    'ugly',
    'big',
    'sad',
    'fat',
    'apple',
    'weird',
    'scary',
    'buffalo',
]

insults_output = [
    "ur face is ",
    "u look like a ",
    "boi ur forehead is ",
    "ur mum is ",
    "boi ur face is ",
    "boi ya look like a ",
]

greetings = [
    "Ooga! Yoshi boogie!",
    "Yoshi! Yoshi!",
    "YOSHI, FAIRY OF DRAGON FLAME!!!",
    "Oogabooga! I ready, and hungry!",
    "YOSHI TO RESCUE!!!",
]

goodbyes = [
    "Scooze me!",
    "This means war!",
    "Nooooooo",
    "Ohhhh.... Yoshi no feel good!",
    "Aww, do I have to go to bed so soon?",
    "Night, Mama Luigi!",
    "Hey! I still hungry!",
]

roast_blacklist = [
    "758086695949434911",
    "316687901884678144",
    "669660483833561110",
]

whitelist = [
    "333025781309767684",
]"""


# ---------------------------------------------------------------------------------------------------------------------------
def random_game_status():
    return discord.Game(name=random.choice(game_list))


def random_song_status():
    return discord.Activity(type=discord.ActivityType.listening, name="Spotify")



def get_insp_quote(person):
    omit = ["i", "me", "he", "she", "her", "him"]
    json_res = requests.get("https://zenquotes.io/api/random").json()
    quote = json_res[0]['q']
    # author = json_res[0]['a']
    inspire = "{0}".format(quote)
    return person.capitalize() + ". " + inspire if person.lower() not in omit else "" + inspire



def photo_searcher_cat():
    cat_photo_res = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]
    cat_photo_url = cat_photo_res['url']
    cat_photo_width = cat_photo_res['width']
    cat_photo_height = cat_photo_res['height']
    cat_fact = requests.get("https://catfact.ninja/fact").json()['fact']
    embed = discord.Embed(
        title='Fun Fact 🐈',
        description=cat_fact,
        colour=discord.Colour.purple(),
        width=cat_photo_width,
        height=cat_photo_height
    )
    embed.set_image(url=cat_photo_url)
    embed.set_footer(text="")
    return embed


def get_joke():
    return requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()['joke']



# ---------------------------------------------------------------------------------------------------------------------------


@client.event
async def on_message(message):
    global isActive

    # Check status
    if message.content.startswith("yoshii status"):
        await message.channel.send("I'm awake!" if isActive else "I'm asleep...zZzZzZ")


    # Do these only when active
    if isActive:
        # print(message.author.name, message.author.id, type(message.author.id))
        # Prevent infinite loop
        if message.author == client.user:
            return



        # Random cat photos
        elif message.content.startswith("yoshii cat"):
            await message.channel.send(embed=photo_searcher_cat())

        # Random joke
        elif message.content.startswith("yoshii tell a joke"):
            await message.channel.send(get_joke())




# ---------------------------------------------------------------------------------------------------------------------------
keep_alive()
client.run((''))