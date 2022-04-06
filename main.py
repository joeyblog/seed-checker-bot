import discord
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import pla

token = 'tototot0_kenkenkenken' #your bot token here
limitChannel = True #if only below channel or all
channelId = 999333335555511111 # replace this with the channel ID you like

seedhash = json.load(open('./static/resources/seedhashes.json', 'r'))

def getHashAndNext(name):
    for pokemon in seedhash:
        if(pokemon["species"]==name):
            return pokemon["hash"], pokemon["allspecies"]
    return "", ""

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game("Python"))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if(limitChannel):
        if(message.channel.id != channelId):
            return

    if(message.content.startswith("search")):
        args = message.content[len("search "):].split()
        #search 4 Piplup 9 6 A SEED
        args0 = int(args[0])
        if(args0 < 0 and args0 > 4):
            await message.channel.send("Shiny roll must be within 0-4!")
            return
        rolls=[13,14,16,17,19]
        roll = rolls[args0] #13,14,16,17,19
        print("roll: "+str(roll))
        print("seed: "+seed)
        args2 = int(args[2])
        args3 = int(args[3])
        if(args2 < 8 and args2 > 10):#8,9,10
            await message.channel.send("First spawns must be within 8-10!")
            return
        if(args3 < 6 and args3 > 7):#6,7
            await message.channel.send("Bonus spawns must be 6 or 7!")
            return
        frnum = args2
        brnum = args3
        print("frnum: "+str(frnum))
        print("brnum: "+str(brnum))
        isbonus = True
        poke = getHashAndNext(args[1]) #Piplup
        frPoke = poke[0]
        if(args[4]=="A"):
            next = poke[1][0]
            brPoke = getHashAndNext("Alpha "+next)[0]
        elif(args[4]=="b"):
            next = poke[1][1]
            brPoke = getHashAndNext(next)[0]
        elif(args[4]=="B"):
            next = poke[1][1]
            brPoke = getHashAndNext("Alpha "+next)[0]
        else:
            await message.channel.send("Specify bonus Pokemon with (A=same alpha, b=evolved, B=evoled alpha).")
            return
        
        seed = args[5]

        await message.channel.send("Searching")
        results = pla.check_from_seed(seed,roll,frPoke, brPoke, isbonus, frnum, brnum)["0 Truebonus"]

        for group in results.keys():
            for pokemon in results[group].keys():
                result = results[group][pokemon]
                #print(result)
                if not result["shiny"]:
                    continue
                
                sprite = "static/img/sprite/" + result["sprite"]
                species = result["species"]
                gender = result["gender"]
                h = str(result["ivs"][0])
                a = str(result["ivs"][1])
                b = str(result["ivs"][2])
                c = str(result["ivs"][3])
                d = str(result["ivs"][4])
                s = str(result["ivs"][5])
                if(h=="31"):
                    h="**31**"
                if(a=="31"):
                    a="**31**"
                if(b=="31"):
                    b="**31**"
                if(c=="31"):
                    c="**31**"
                if(d=="31"):
                    d="**31**"
                if(s=="31"):
                    s="**31**"
                nature = result["nature"]
                statsChange = {
                    "Lonely":{"up":"a", "down":"b"}, 
                    "Adamant":{"up":"a", "down":"c"}, 
                    "Naughty":{"up":"a", "down":"d"}, 
                    "Brave":{"up":"a", "down":"s"}, 

                    "Bold":{"up":"b", "down":"a"}, 
                    "Impish":{"up":"b", "down":"c"}, 
                    "Lax":{"up":"b", "down":"d"}, 
                    "Relaxed":{"up":"b", "down":"s"}, 

                    "Modest":{"up":"c", "down":"a"}, 
                    "Mild":{"up":"c", "down":"b"}, 
                    "Rash":{"up":"c", "down":"d"}, 
                    "Quiet":{"up":"c", "down":"s"}, 

                    "Calm":{"up":"d", "down":"a"}, 
                    "Gentle":{"up":"d", "down":"b"}, 
                    "Careful":{"up":"d", "down":"c"}, 
                    "Sassy":{"up":"d", "down":"s"}, 

                    "Timid":{"up":"s", "down":"a"}, 
                    "Hasty":{"up":"s", "down":"b"}, 
                    "Jolly":{"up":"s", "down":"c"}, 
                    "Naive":{"up":"s", "down":"d"}, 
                }
                if nature in statsChange:
                    up = statsChange[nature]["up"]
                    down = statsChange[nature]["down"]
                    upSymble = "↑"
                    downSymble = "↓"
                    if(up =="a"):
                        a += " "+upSymble
                    if(up =="b"):
                        b += " "+upSymble
                    if(up =="c"):
                        c += " "+upSymble
                    if(up =="d"):
                        d += " "+upSymble
                    if(up =="s"):
                        s += " "+upSymble
                    if(down =="a"):
                        a += " "+downSymble
                    if(down =="b"):
                        b += " "+downSymble
                    if(down =="c"):
                        c += " "+downSymble
                    if(down =="d"):
                        d += " "+downSymble
                    if(down =="s"):
                        s += " "+downSymble
                path = BeautifulSoup(result["index"], 'html.parser').get_text()
                if(gender == "Genderless"):
                    name = species
                elif(gender == "Male"):
                    name = species + " ♂"
                elif(gender == "Female"):
                    name = species + " ♀"
                desc = "HP : "+h +"\n"+"Atk: "+a+"\n"+"Def: "+b+"\n"+"SpA: "+c+"\n"+"SpD: "+d+"\n"+"Spe: "+s
                desc = desc + "\n\n"+path
                
                embedVar = discord.Embed(title=name,description=desc)
                file = discord.File(sprite, filename="image.png")
                embedVar.set_thumbnail(url="attachment://image.png")
                await message.channel.send(file=file, embed=embedVar)

client.run(token)