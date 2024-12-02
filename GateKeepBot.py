import asyncio
import time
import discord
import os
import cloudmersive_virus_api_client as cloudmersive
from dotenv import load_dotenv

# API configuration stuff. V = virus API, D = Discord API
authV = cloudmersive.ScanApi()
authV.api_client.configuration.api_key['Apikey'] = 'CLOUDMERSIVE API KEY'
authD = 'DISCORD BOT TOKEN'
# IMPORTANT: THIS IS INSECURE. SECURITY UPDATE COMING SOON
# Unimplimented code to scan links, easy to impliment coming soon
#link_result = virus_instance.WebsiteScanRequest(web_link)
#web_link = #varible


# Security stuff, not yet in use
load_dotenv()
#Consider putting discord token in another file
#os.getenv('DISCORD_TOKEN')

#Initalizes or starts up the communication to discord
intents = discord.Intents.default()
intents.message_content = True
clientD = discord.Client(intents = intents)

@clientD.event
async def on_message(message):
    if message.author == clientD.user:
        pass
    for attachments in message.attachments:
        FilePath = f'./{attachments.filename + clientD.user.id + time.ctime}'
        await attachments.save(FilePath)
        # put this print function in a log file
        print(attachments.save(FilePath), time.ctime)
        #This will delete the file
        scan_result = authV.scan_file(FilePath)
        await scan_result
        os.remove(FilePath)
        print("file deleted @", time.ctime)
        if scan_result["CleanResult"] == 'true':
            pass
        else:
            await message.delete
            await message.channel.send(f'@Mentors {message.author} has sent a file that has been found to be a virus')


clientD.run(authD)