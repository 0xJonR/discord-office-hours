#! /usr/bin/python
import discord
import sys
from discord.ext import commands
from collections import defaultdict


def isTA(usr: discord.Member):
    roles = usr.roles
    for x in roles:
        if x.name.upper() == "CSE 116 TA":
            return True
    return False

def sanitizeString(s):
    needToEscape = ["*", "`", "~", "_", ">", "|", ":"]  # Characters that need to have an excape character placed in front of them
    needToRemove = ["\\", "/", "."]  # Characters that need to be replaced with a space
    for char in needToEscape:
        s = s.replace(char, "\\" + char)
    for char in needToRemove:
        s = s.replace(char, " ")
    while "  " in s:  # Remove double spaces
        s = s.replace("  ", " ")
    return s

def printQ(q):
    st = "Queue is:\n"
    for x, ele in enumerate(q):
        nickname = ele.nick
        username = sanitizeString(ele.name)  # Sanitize input to prevent formatting
        if nickname:
            nickname = sanitizeString(nickname)
            st += "{}. {} ({})\n".format(x + 1, nickname, username)
        else:
            st += "{}. {}\n".format(x + 1, username)
    return st


client = discord.Client()
id_to_list = {}  # string->List dictionary


@client.event
async def on_ready():  # onready is called after all guilds are added to client
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global id_to_list
    thisid = str(message.guild.id)
    if message.author == client.user:
        return  # prevents infinite loops of reading own message

    if message.channel.name == "office-hours-queue":  # only want messages in OH

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
                    if len(queue) == 0:
                        msg = "{} you have been successfully added to the queue, and you are first in line!".format(name)
                        queue.append(stu)
                        await message.channel.send(msg)
                    else:
                        queue.append(stu)
                        msg = "{} you have been successfully added to the queue in position: {}".format(name, len(queue))
                        await message.channel.send(msg)
            else:
                queue = [stu]
                id_to_list[thisid] = queue
                msg = "{} you have been successfully added to the queue, and you are next!".format(name)
                await message.channel.send(msg)

        #               leave queue
        if message.content.startswith('!leave') or message.content.startswith('!L'):
            stu = message.author
            name = stu.mention
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if stu in queue:
                    queue.remove(stu)
                    msg = "{} you have successfully removed yourself from the queue.".format(name)
                    await message.channel.send(msg)
                else:
                    msg = "{}, according to my records, you were already not in the queue.".format(name)
                    await message.channel.send(msg)
            else:
                # leave called before any enqueues
                print("edge case")
                msg = "{}, according to my records, you were already not in the queue.".format(name)
                await message.channel.send(msg)

        if message.content.startswith('!cal'):
            msg = "Here's the Office Hours schedule on Piazza. https://piazza.com/class/kk305idk4vd72?cid=6"
            await message.channel.send(msg)

        #               dequeue: TA only
        if (message.content.startswith('!dequeue') or message.content.startswith('!D')) and isTA(message.author):
            ta = message.author.mention
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if len(queue) > 0:
                    stu = queue.pop(0)
                    msg = "{}, you are next! {} is available to help you now!".format(stu.mention, ta)
                    await message.channel.send(msg)
                else:
                    # no one in queue
                    msg = "Good job TAs! The Queue is empty!"
                    await message.channel.send(msg)
            else:
                # called before anyone enqueued
                msg = "Good job TAs! The Queue is empty!"
                await message.channel.send(msg)

        #           Clear queue: TA only
        if (message.content.startswith('!clearqueue') or message.content.startswith('!C')) and isTA(message.author):
            id_to_list[thisid] = []
            msg = "Cleared the queue."
            await message.channel.send(msg)

        #              show queue
        if message.content.startswith('!show') or message.content.startswith(
                '!showqueue') or message.content.startswith('!S'):
            if thisid in id_to_list:
                queue = id_to_list[thisid]
                if queue:
                    # printQ
                    msg = printQ(queue)
                    await message.channel.send(msg)
                else:
                    msg = "The queue is empty right now."
                    await message.channel.send(msg)
            else:
                msg = "The queue is empty right now."
                id_to_list[thisid] = []
                await message.channel.send(msg)

        # help
        if message.content.startswith('!help'):
            msg = '''To enqueue yourself, send a "!enqueue" or "!E" message.\nTo see the current Queue, send a "!show" or "!S" message.\nTA's will dequeue you with a "!dequeue" or "!D" message.\nTo leave the queue, you can use "!leave" or "!L".\nYou can view the office hours schedule with "!cal". \nThis bot is still in development and might have some minor issues. It was deployed in a rush.'''
            await message.channel.send(msg)

    # else:  # Not in office hours channel
    #     if message.content.lower().startswith('!panik'):
    #         await message.channel.send("https://media.discordapp.net/attachments/542843013559353344/692393206205251744/PANIK.gif")

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