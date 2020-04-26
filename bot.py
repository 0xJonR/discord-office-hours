#! /usr/bin/python
import discord
import sys
from discord.ext import commands
from collections import deque

client = discord.Client()


TAID= "539163810796142596"
officeHoursChannelID="688099265314029735"

studentsQ = [] #of type discord.Member

def isTA(usr: discord.Member):
	roles = usr.roles
	for x in roles:
		if x.id == TAID:
			return True
	return False

def printQ():
    st = "Queue is:\n"
    for ele in studentsQ:
        st += ele.name
        st += '\n'
    return st


def putStudentInBack(badBoy: discord.Member, currentQueue):
    newQueue = []
    for stud in currentQueue:
        if stud == badBoy:
            # donothing
            print("Spam Alert")
        else:
            newQueue.append(stud)
    newQueue.append(badBoy)
    return newQueue


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global studentsQ
    # here we do all logic for message events
    if message.author == client.user:
        return
    # prevents infinite loops of reading own message

    if message.channel.name == "office-hours-queue":
        # only want messages in OH
        # enqueue
        if message.content.startswith('!enqueue') or message.content.startswith('!E'):
            # await message.channel.send('Hello'!)
            stu = message.author
            name = stu.mention
            if stu in studentsQ:
                # do put student in back of the queue
                studentsQ = putStudentInBack(stu, studentsQ)
                response = "{} You were already in the queue! You've been moved to the back.".format(stu.mention)
                await message.channel.send(response)
            else:
                studentsQ.append(stu)
                # print('Recieved message')
                response = "Enqueued {} successfully. Position in Queue: {}".format(name, len(studentsQ))
                await message.channel.send(response)

        if message.content.startswith('!leave') or message.content.startswith('!L'):
            stu = message.author
            name = stu.mention
            if stu in studentsQ:
                # Remove ths student from the queue
                studentsQ.remove(stu)
                response = "You've been removed from the queue, {}!".format(name)
                await message.channel.send(response)
            else:
                # The student wasn't in the queue to begin with
                response = "You weren't in the queue, {}.".format(name)
                await message.channel.send(response)

        # dequeue: TA only
        if (message.content.startswith('!dequeue') or message.content.startswith('!D')) and isTA(message.author):
            if len(studentsQ) > 0:
                stu = studentsQ.pop(0)
                msg = "{}, you are next! {} will help you now!".format(stu.mention, message.author.mention)
                await message.channel.send(msg)
            else:
                await message.channel.send("Queue is empty! Good job!")


        # Clear queue: TA only
        if (message.content.startswith('!clearqueue') or message.content.startswith('!C')) and isTA(message.author):
            if len(studentsQ) > 0:
                studentsQ = []
                msg = "The queue has been cleared!"
                await message.channel.send(msg)
            else:
                await message.channel.send("There is nobody in the queue.")

        # show queue
        if message.content.startswith('!show') or message.content.startswith(
                '!showqueue') or message.content.startswith('!S'):
            if (not studentsQ):
                await message.channel.send("Wow! The queue is empty right now!")  # not studentsQ is if empty
            else:
                msg = printQ()
                await message.channel.send(msg)

        if message.content.startswith('!help'):
            msg = ''' To enqueue yourself, send a "!enqueue" or "!E" message. To see the current Queue, send a "!show" or "!S" message. TA's will dequeue you with a "!dequeue" or "!D" message. To leave the queue, you can use !leave or !L.'''
            await message.channel.send(msg)

    # TODO:


# if message.content.startswith('!room'):
# create new role for student being helped
# allow only that student and TAs in that room
# max rooms = n
# have a ~!close message to close a room

if __name__ == "__main__":
    mytoken = sys.argv[1]
    studentsQ = []
    client.run(mytoken)  # TODO: system env to run from a bat script to keep my token safe online
    main()

