import re
from utils import setRemindTime
from db import setReminder, getUserReminders
from discord import Embed

async def createReminder(message):
  times = re.findall("[1-9][0-9]*[ymwdhMs]+", message.content)

  if len(times) < 1:
    msg = "Invalid format. Use '!reminder [time until reminder] [message]'\nHere is an example to set a reminder for 3 hours and 15 minutes from now.\n!reminder 3h15m hello world"

    await message.author.send(msg)
    
    return

  textMessage = ' '.join(
  message.content.split()[2:])
  remindTime = setRemindTime(times)
  formattedTime = remindTime.strftime("%Y-%m-%d %H:%M:%S")
  
  setReminder(formattedTime, message.author.id, textMessage, message.author.display_name, message.channel.id)
 
  await message.channel.send(f"Reminder set for {formattedTime}")

async def listUserReminders(message):
  
  reminders = getUserReminders(message.author.id)
  description = "{author} has {length} {reminderS} scheduled.".format(reminderS="reminders" if len(reminders) != 1 else "reminder", length = len(reminders), author=message.author.display_name)

  embedVar = Embed(title=description)
  reminderText = ""
  timeStampText = ""
  
  for reminder in reminders:
    reminderText += f"{reminder['message']}\n"
    timeStampText += f"{reminder['time']}\n"

  if (len(reminderText) > 0):
    embedVar.add_field(name = "Reminder", value=reminderText, inline=True)
    embedVar.add_field(name="Created At", value=timeStampText, inline=True)
  
  await message.channel.send(embed = embedVar)
  