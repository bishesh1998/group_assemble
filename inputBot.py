import os
import discord
from dotenv import load_dotenv

import parsers
import grouper
import asyncio

load_dotenv()


#The discord token should be in .env file
#DISCORD_TOKEN= tOkenHer3
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

picker = {}
receiver = {}
roles = []
categories = []
newChannels = []
newVoices = []

@client.event
async def on_message(message):
    global picker, receiver, roles, categories, newChannels, newVoices
    content = message.content.strip().split()

    #if here is no content or the message is from the bot itself, ignore it.
    if len(content) < 1:
        return
    if message.author == client.user:
        return

    #this print out the help message
    if content[0] == "~help":
        await message.channel.send("""
Welcome to project group Generator!
Set reference: `~addReference <Group index (0-1)> <name of picker> <name of person>`
Edit reference: `~editReference <Group index (0-1)> <name of picker> <index of reference> <name of person>`
Import reference: `~importReference <Group index (0-1)> <name of picker> <list of people, seperated by space>`
Clear reference: `~clearReference <Group index (0-1)> <name of the person to clear reference>`
Reset all: `~resetAll`
Run the algoritm: `~runGroup`
        """)


    if content[0] == "~test":
        message.author.add_roles()

    #add a single reference to a person
    if content[0] == "~addReference":
        if content[1] == "0":
            if content[2] in picker:
                #content[1] is name of picker
                picker[content[2]].append(content[3])
            else:
                picker[content[2]] = [content[3]]
        else:
            if content[2] in receiver:
                #content[1] is name of picker
                receiver[content[2]].append(content[3])
            else:
                receiver[content[2]] = [content[3]]

        #react to message
        await message.add_reaction('✅')


    #edit reference of a person
    elif content[0] == "~editReference":
        if content[1] == "0":
            if content[2] not in picker:
                await message.channel.send(f"{content[2]} doesn't have any reference!")
            else:
                if len(picker[content[2]]) <= (int(content[3]) + 1):
                    #replace reference
                    picker[content[2]][content[3]] = content[4]

                else:
                    await message.channel.send(f"{content[1]} doesn't have that many referenecs!")
        else:
            if content[2] not in receiver:
                await message.channel.send(f"{content[2]} doesn't have any reference!")
            else:
                if len(receiver[content[2]]) <= (int(content[3]) + 1):
                    #replace reference
                    receiver[content[2]][content[3]] = content[4]
                else:
                    await message.channel.send(f"{content[1]} doesn't have that many referenecs!")

        #react to message
        await message.add_reaction('✅')

    
    #clear a reference from a person
    elif content[0] == "~clearReference":
        if content[1] == "0":
            if content[2] in picker:
                picker[content[2]] == []
            
            else: # if the person is not found in the dictionary
                await message.channel.send("No person can be found")
        
        elif content[1] == "1":
            if content[2] in receiver:
                receiver[content[2]] == []
            else:
                await message.channel.send("No person can be found")
        
        #react to message
        await message.add_reaction('✅')
    
    #add multiple reference to a single person
    elif content[0] == "~importReference":
        if content[1] == "0":

            # if the person is already in the dictionary, append to the list of reference, if not create a new list
            if content[2] in picker:
                for i, name in enumerate(content):
                    if i > 2:
                        picker[content[2]].append(name)

            else:
                picker[content[2]] = []
                for i, name in enumerate(content):
                    if i > 2:
                        picker[content[2]].append(name)
        
        else:
            if content[2] in receiver:
                for i, name in enumerate(content):
                    if i > 2:
                        receiver[content[2]].append(name)

            else:
                receiver[content[2]] = []
                for i, name in enumerate(content):
                    if i > 2:
                        receiver[content[2]].append(name)

        #react to message
        await message.add_reaction('✅')

    # reset all the reference
    elif content[0] == "~resetAll":
        picker = {}
        receiver = {}
        #react to message
        await message.add_reaction('✅')

    # delete the role and all the channel related to this run
    elif content[0] == "~cleanUp":
        try:
            for i in newChannels:
                await i.delete()
        except Exception as e:
            print(e)

        try:
            for i in newVoices:
                await i.delete()
        except Exception as e:
            print(e)
        
        try:
            for i in categories:
                await i.delete()
        except Exception as e:
            print(e)

        try:
            for i in roles:
                await i.delete()
        except Exception as e:
            print(e)


    # run the algorithm
    elif content[0] == "~runGroup":
        #get the current server.
        currentGuild = client.get_guild(653133437087121419)

        #run th algorithm
        parseResult = parsers.parseInput(picker, receiver)

        groupResult = grouper.grouping(parseResult[0], parseResult[1])

        # parse the output
        parsedOutput = parsers.parseOutput(picker, receiver, groupResult)

        print(parsedOutput)
        
        # this will count the number of group
        i = 0

        # loop through every group
        # x, y is the 2 name of the people in the group
        for x,y in parsedOutput.items():
            i += 1
            
            #print out the group index and the 2 name of the member
            await message.channel.send(f"Group {i} have these members: {x}, {y}")
            
            # Try to create role and create text channel for these member.
            try:
                #try:
                    #get 2 user: user1
                roles.append (await message.guild.create_role(name = f"Group {i}"))
                user1 = currentGuild.get_member(int(x[3:-1]))
                user2 = currentGuild.get_member(int(y[3:-1]))

                

                #await asyncio.sleep(0.3)
                await user1.add_roles(roles[-1])
                await user2.add_roles(roles[-1])

                #create text Channel
                categories.append(await currentGuild.create_category(f"Group {i}"))
                await asyncio.sleep(0.3)
                newChannels.append(await currentGuild.create_text_channel(f"Group {i} text", category = categories[-1]))
                newVoices.append(await categories[-1].create_voice_channel(f"Group {i} voice"))



            except Exception as e:
                print(e)
            # except Exception as e:
            #     print(e)

        #react to message
        await message.add_reaction('✅')


        #print(picker[content[2]])
    

    print(picker)
    print(receiver)

# parseResult = parsers.parseInput(picker, receiver)

# groupResult = grouper.grouping(parseResult[0], parseResult[1])

client.run(TOKEN)



#test case
# {'A': ['0', '3', '2', '1'], 'B': ['2', '3', '1', '0'], 'C': ['0', '2', '1', '3'], 'D': ['1', '2', '0', '3']}
# {'0': ['A', 'B', 'C', 'D'], '1': ['B', 'C', 'D', 'A'], '2': ['B', 'D', 'A', 'C'], '3': ['A', 'C', 'B', 'D']}