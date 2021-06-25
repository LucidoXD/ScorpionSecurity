import re
from bot.assistant import *
from telethon import events, Button
import heroku3
import asyncio
import os
import requests
from bot.assistant import NAME
from datetime import datetime
from telethon import events
from bot.Config import Var
from telegraph import Telegraph, upload_file

########--Config--#########
LOAD_MYBOT = Var.LOAD_MYBOT
Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
BOT_PIC = Var.BOT_PIC if Var.BOT_PIC else "https://telegra.ph/file/cfa9f7a1c17ad72e03559.jpg"
heroku_api = "https://api.heroku.com"
path = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(path):
    os.makedirs(path)
telegraph = Telegraph()
r = telegraph.create_account(short_name=Var.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]
  ####--ENDED--####

# start-others

@bot.on(events.NewMessage(pattern="^/start"))
async def start_all(event):
    if event.chat_id == OWNER_ID:
        return
    target = event.sender_id
    if present_in_userbase(target):
        pass
    else:
        try:
            add_to_userbase(target)
        except BaseException:
            pass
    if LOAD_MYBOT == "False":
            await bot.send_file(event.chat_id,
                                  BOT_PIC,
                                  caption=startother, 
                                  Button=[
                [Button.inline("What can i do🤔", data="what"),
                Button.inline("What is this❓", data="know")]
             ]
           )
                                  
    else:
            await bot.send_file(event.chat_id, BOT_PIC, caption=startother, Button=[
                [Button.inline("What can i do🤔", data="what"),
                Button.inline("What is this❓", data="know")]
             ]
           )
             
@bot.on(events.callbackquery.Callbackquery(data=re.compile(b"what")))
async def what(event): 
        await event.edit(f"H!👀\n You can Talk to my master {USERNAME} through me..If He is NoT responding you in PM OR if you Got blocked😂You can talk to him through me😗 that's it")
        
@bot.on(events.callbackquery.Callbackquery(data=re.compile(b"know")))
async def know(event): 
        await event.edit(f"I am a PM_BOT maded With Python...I can help to protect from scammers in PM's via my PM_SECURITY and From Here you can talk to my master also\nI have some special features also like:-\n •PM_PIC\n •ASSISTANT_PIC\n •CUSTOM MESSAGES etc. You also want?👀Deploy Your Own by clicking below👀:", 
          Button=[
                    [Button.url("Repository✨", "https://github.com/PsychoBots/ScorpioneScurity"), 
                    Button.url("DEPLOY NOW💠", "https://heroku.com/deploy?template=https://github.com/PsychoBots/ScorpionSecurity"), 
                    Button.inline("Support For Help👥", data="sup")
                    ]
                  ]
                )
                
@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"sup")))
async def support(event):
        await event.edit(f"BELOW IS Our Support group and Channel... Report Errrors AT chat group:", 
          Button=[
              [Button.url("CHAT GROUP💭", "https://t.me/PsychoBots_Chat")],
              
              [Button.url("Official Channel📡", "https://t.me/Psycho_Bots")
                    ],
                 ],
              )
              
              
#####start by OWNER #######


@bot.on(events.NewMessage(pattern="^/start", from_users=OWNER_ID))  
async def owner(event):
    await bot.send_message(event.chat_id,
                             startowner,
                             Button=[
                    
                      [Button.inline("⚒️Settings⚒️", data="sett"),
                      Button.inline("SUPPORT👑", data="supp"),
                      ]
                             ])
                      
@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"supp")))
async def support(event):
    if event.sender_id == OWNER_ID:
      
        await event.edit(f"BELOW IS Our Support group and Channel... Report Errrors AT chat group:", 
          Button=[
              [Button.url("CHAT GROUP💭", "https://t.me/PsychoBots_Chat")],
              
              [Button.url("Official Channel📡", "https://t.me/Psycho_Bots")
                    ],
                ],
            )



@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"sett")))
async def sett(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        ok = Var.BOT_USERNAME
        if ok.startswith('@'):
            ok = ok.split('@')[1]
        await bot.send_message(event.chat_id, "HELLO! sir how can I help you today..\n\nSettings👀 Options are below choose😗:", Button=[
                          [Button.inline("BOT_PIC🖼", data="pic"),
                          Button.inline( "PM BOT", data="custom")]
                          ])
                      
    else:
        await event.answer("Make your own @PsychoBots_Chat ←SUPPORT", alert=True)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pic"))
          )  # pylint: disable=oof
async def bot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("SEND THE PICTURE 🖼️that you want to show when someone Start me😗")
            await conv.send_message("Send /cancel to STOP🙄")
            response = await conv.get_response()
            try:
                themssg = response.message.message
                if themssg == "/cancel":
                    await conv.send_message("😂OK...I stoped all progress..\n\n~BYE!!")
                    return
            except BaseException:
                pass
            media = await event.client.download_media(response, "Bot_Pic")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Error!")
        bot = "BOT_PIC"
        if Var.HEROKU_APP_NAME is not None:
            app = Heroku.app(Var.HEROKU_APP_NAME)
        else:
            mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        xx = await bot.send_message(event.chat_id, "Changing your Bot Pic, please wait for a minute")
        heroku_var = app.config()
        heroku_var[bot] = f"{url}"
        mssg = f"Successfully changed your bot pic. Please wait for a minute.\n"
        await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"custom")))
    if event.sender_id == OWNER_ID:
        await event.reply(event.chat_id, "WHAT YOU WANNNA TO CHANGE IN YOUR PM SECURITY BOT👀", Button=[
                              Button.inline("PM PIC🖼️", data="pmpic"), 
                              Button.inline("PM TEXT", data="pmtext")]
                              )

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmtext")))
async def a_txt(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        old_alv= Var.DM_TEXT if Var.DM_TEXT else "Default PMSecurity message"
        tgbot="DM_TEXT"
        if Var.HEROKU_APP_NAME is not None:
            app=Heroku.app(Var.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send the text which you want as your PMSecurity Message!\nUse /cancel to cancel the operation.")
            response=conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response=await response
            themssg=response.message.message
            if themssg == None:
                await conv.send_message("Error!")
                return
            if themssg == "/cancel":
                await conv.send_message("Cancelled!!")
            heroku_var=app.config()
            xx = await bot.send_message(event.chat_id, "Changing your PMSecurity Message, please wait for a minute")
            heroku_var[tgbot]=f"{themssg}"
            mssg=f"Changed your PMsecurity Message sucessfully to\n`{themssg}`\n"
            await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmpic")))
async def alv_pic(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await bot.send_message(event.chat_id, "Send me a pic so as to set it as your PMSecurity pic.")
        async with event.client.conversation(OWNER_ID) as conv:
            await conv.send_message("Send /cancel to cancel the operation!")
            response = await conv.get_response()
            try:
                themssg=response.message.message
                if themssg == "/cancel":
                    await conv.send_message("Operation cancelled!!")
                    return
            except:
                pass
            media=await event.client.download_media(response, "PM_PIC")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Error!")
        tbot="PMPERMIT_PIC"
        if Var.HEROKU_APP_NAME is not None:
            app=Heroku.app(Var.HEROKU_APP_NAME)
        else:
            mssg="`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        xx = await bot.send_message(event.chat_id, "Changing your PMSecurity Pic, please wait for a minute")
        heroku_var=app.config()
        heroku_var[tbot]=f"{url}"
        mssg=f"Successfully changed your PMSecurity pic. Please wait for a minute.\n"
        await xx.edit(mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)
