# discord-office-hours
Discord Bot that implements an automatic queue for students to enqueue themselves.
<br>**Note**: Bot only looks for messages sent in a channel called "office-hours-queue"

## List of commands: 
* !Enqueue or !E 
  <br> Enqueues sender of message onto queue. All permissions are allowed to enqueue themselves. If one is already on the queue, sends them to the bottom.
  
* !Dequeue or !D
  <br> Dequeues head of queue, and sends a mention to the user in the channel that they're ready to be helped. **Only works if sent by user with TA role**.
  
* !show or !S
  <br> Shows the queue with names of those in it without using mentions. 

* !help
  <br> Shows all usable commands.

## Installation 
*  execute in terminal: "python3 bot.py [your_dicsord_bot_token]" 
