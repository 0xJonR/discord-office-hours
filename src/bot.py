#! /usr/bin/python
import discord 
import sys
from discord.ext import commands
from collections import deque

client = discord.Client()

studentsQ = []

def isTA(usr: discord.Member):
	roles = usr.roles
	for x in roles:
		if x.name == "TA":
			return True
	return False

def printQ():
	st = "Queue is:\n"
	for ele in studentsQ:
		st += ele
		st += '\n'
	return st

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	#here we do all logic for message events
	if message.author == client.user:
		return 
		#prevents infinite loops of reading own message

	if message.channel.name == "office-hours-queue":
# only want messages in OH		
					#enqueue
		if message.content.startswith('!enqueue') or message.content.startswith('!E'):
			#await message.channel.send('Hello'!)
			stu = message.author
			name = stu.mention
			studentsQ.append(name)
			#print('Recieved message')
			response = "Enqeueued {} successfully. Position in Queue: {}".format(name, len(studentsQ))
			await message.channel.send(response)

					#dequeue: TA only 
		if (message.content.startswith('!dequeue') or message.content.startswith('!D')) and isTA(message.author):
			if len(studentsQ) > 0:
				stu = studentsQ.pop(0)
				msg = "{}, you are next! {} will help you now!".format(stu, message.author.mention)
				await message.channel.send(msg)
			else:
				await message.channel.send("Queue is empty! Good job!")


					#show queue
		if message.content.startswith('!show') or message.content.startswith('!showqueue') or message.content.startswith('!S'):
			if(not studentsQ):
				await message.channel.send("Wow! The queue is empty right now!") #not studentsQ is if empty
			else:
				msg = printQ()
				await message.channel.send(msg)


		if message.content.startswith('!help'):
			msg = ''' To enqueue yourself, send a "!enqueue" or "!E" message. To see the current Queue, send a "!show" or "!S" message. TA's will dequeue you with a "!dequeue" or "!D" message. '''
			await message.channel.send(msg)


#		if message.content.startswith('!room'):
#			message.guild.

if __name__ == "__main__":
	mytoken = sys.argv[1]
	client.run(mytoken)		#TODO: system env to run from a bat script to keep my token safe online
	main()