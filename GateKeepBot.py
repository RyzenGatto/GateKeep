import asyncio
import pprint
import time
import discord
import os
import cloudmersive_virus_api_client as cloudmersive
from dotenv import load_dotenv

# API configuration stuff. V = virus API, D = Discord API
authV = cloudmersive.ScanApi()
authV.api_client.configuration.api_key['Apikey'] = 'CLOUDMERSIVE API KEY'
authD = 'DISCORD API KEY'
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

    TS = 1

    if message.author == clientD.user:
        pass

    for attachments in message.attachments:
        FilePath = f'./{clientD.user.id}_{time.strftime("%d_%m_%Y %H.%M.%S", time.localtime())}_{attachments.filename}'
        await attachments.save(FilePath)

        print("File saved", FilePath, time.ctime()) # put this print function in a log file

        while True: #This loop will make sure that the file is saved before continuing with the script
            if os.path.exists(FilePath):
                break
            else:
                TS += 1
                print("file not found, awaiting %d seconds", TS)
                time.sleep(TS)

        scan_result = authV.scan_file(FilePath) 
     
        
        print(scan_result)
        
    count = 0

    if hasattr(scan_result,"clean_result") and scan_result.clean_result is True:
        print("No virus found")
        pass
    else:
        message.delete()
        message.channel.send(f'@Mentors {message.author} has sent a file that has been found to be a virus')
        print(scan_result.found_viruses)


    while True:
        if os.path.exists(FilePath):
            count += 1
            if count > 1:
                print(count)
            os.remove(FilePath)
        else:
            break

clientD.run(authD)