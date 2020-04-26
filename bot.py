#! /usr/bin/python
import discord
import sys
from discord.ext import commands
from collections import defaultdict

def isTA(usr: discord.Member):
    roles = usr.roles
    for x in roles:
        if x.name == "TA":
            return True
    return False

def printQ(q):
    st = "Queue is:\n"
    for ele in q:
        st += ele.name
        st += '\n'
    return st

client = discord.Client()
id_to_list = {} #string->List dictionary


@client.event
async def on_ready(): #onready is called after all guilds are added to client
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    global id_to_list            
    thisid = str(message.guild.id)
    if message.author == client.user:
        return # prevents infinite loops of reading own message

    if message.channel.name == "office-hours-queue": # only want messages in OH

        #               enqueue
        if message.content.startswith('!enqueue') or message.content.startswith('!E'):
            stu = message.author
            name = stu.mention
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if stu in queue:
                    queue.remove(stu)
                    queue.append(stu)
                    msg = "{} you were already in the list! You have been moved to the back.".format(name)
                    await message.channel.send(msg)
                else:
                    if(len(queue) == 0):
                        msg = "{} you have been succesfully added to the queue, and you are first in line!".format(name)
                        queue.append(stu)
                        await message.channel.send(msg)
                    else:   
                        queue.append(stu)
                        msg = "{} you have been succesfully added to the queue in position: {}".format(name, len(queue))
                        await message.channel.send(msg)
            else:
                queue = [stu]
                id_to_list[thisid] = queue
                msg = "{} you have been succesfully added to the queue, and you are next!".format(name)
                await message.channel.send(msg)

            
        #               leave queue
        if message.content.startswith('!leave') or message.content.startswith('!L'):
            stu = message.author
            name = stu.mention
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if stu in queue:
                    queue.remove(stu)
                    msg = "{} you have succesfully removed yourself from the queue.".format(name)
                    await message.channel.send(msg)
                else:
                    msg = "{}, according to my records, you were already not in the queue.".format(name)
                    await message.channel.send(msg)
            else:
                #leave called before any enqueues
                print("edge case")
                msg = "{}, according to my records, you were already not in the queue.".format(name)
                await message.channel.send(msg)


        #               dequeue: TA only
        if (message.content.startswith('!dequeue') or message.content.startswith('!D')) and isTA(message.author):
            ta = message.author.mention
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if(len(queue) > 0):
                    stu = queue.pop(0)
                    msg = "{}, you are next! {} is available to help you now!".format(stu.mention, ta)
                    await message.channel.send(msg)
                else:
                    #no one in queue
                    msg = "Good job TAs! The Queue is empty!"
                    await message.channel.send(msg)
            else:
                #called before anyone enqueued
                msg = "Good job TAs! The Queue is empty!"
                await message.channel.send(msg)


        #           Clear queue: TA only
        if (message.content.startswith('!clearqueue') or message.content.startswith('!C')) and isTA(message.author):
            id_to_list[thisid] = []
            msg = "Cleared the list."
            await message.channel.send(msg)

        #              show queue
        if message.content.startswith('!show') or message.content.startswith('!showqueue') or message.content.startswith('!S'):
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if queue:
                    #printQ
                    msg = printQ(queue)
                    await message.channel.send(msg)
                else:
                    msg = "The queue is empty right now."
                    await message.channel.send(msg)    
            else:
                msg = "The queue is empty right now."
                id_to_list[thisid] = []
                await message.channel.send(msg)

        #help
        if message.content.startswith('!help'):
            msg = ''' To enqueue yourself, send a "!enqueue" or "!E" message. To see the current Queue, send a "!show" or "!S" message. TA's will dequeue you with a "!dequeue" or "!D" message. To leave the queue, you can use "!leave" or "!L".'''
            await message.channel.send(msg)

    # TODO:


# if message.content.startswith('!room'):
# create new role for student being helped
# allow only that student and TAs in that room
# max rooms = n
# have a ~!close message to close a room

if __name__ == "__main__":
    mytoken = sys.argv[1]
    client.run(mytoken)  # TODO: system env to run from a bat script to keep my token safe online
    main()

