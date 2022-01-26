import discord
import os
import random
import requests
#from keep_alive import keep_alive

client = discord.Client()

isActive = True

homeworks = {}

insults_output = []

greetings = [
    "おはようございます！",
    "こんにちは",
    "さしぶりね"
]

goodbyes = [
    "さようなら",
    "失礼します",
    "じゃあ、まった",
    "まったね!",
    "ふん。。ふん",

]


# ---------------------------------------------------------------------------------------------------------------------------

def get_homework():
    s = ""
    for key in homeworks:
        s += key + " " + homeworks[key]
        s += "\n"
    return s


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


# ---------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global isActive

    # Check status
    if message.content.startswith("Miko status"):
        await message.channel.send("I'm awake!" if isActive else "I'm asleep...zZzZzZ")

    # Set awake or sleep
    if message.content.startswith("Miko wake up"):
        isActive = True
        await message.channel.send(random.choice(greetings))
    elif message.content.startswith("Miko sleep"):
        isActive = False
        await message.channel.send(random.choice(goodbyes))

    if isActive:
        # print(message.author.name)
        # Prevent infinite loop
        if message.author == client.user:
            return

        # Add to insults_keywords
        elif message.content.startswith("Miko add homework "):
            print(message.content)
            await message.channel.send(message.content.split(' ')[-2] + " added to homework")
            if message.content.split(' ')[-1] not in homeworks:
                homeworks[message.content.split(' ')[-2]] = message.content.split(' ')[-1]

        elif message.content.startswith("Miko homework"):
            if homeworks:
                await message.channel.send(get_homework())
            else:
                await message.channel.send("No homework tonight!")

        # Remove from insults_keywords
        elif message.content.startswith("Miko remove homework "):
            await message.channel.send(message.content.split(' ')[-1] + " removed from homework")
            if message.content.split(' ')[-1] in homeworks:
                del homeworks[message.content.split(' ')[-2]]
            else:
                await message.channel.send("Please put in an existing homework")

        # Random inspirational quotes
        elif message.content.startswith("Miko inspire "):
            await message.channel.send(get_insp_quote(message.content.split(' ')[-1]))

        # Random cat photos
        elif message.content.startswith("Miko cat"):
            await message.channel.send(embed=photo_searcher_cat())

        # Output the list of insults_keywords
        # Default greetings

        # Last condition
        # Listening for insults_keywords


# ---------------------------------------------------------------------------------------------------------------------------
#keep_alive()

client.run((''))