# This file is part of rdt project on github.com/justxd22
import praw, requests, urllib, shutil, os.path, sys, re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ReplyKeyboardMarkup
from random import randint

print("My PID is:", os.getpid())
PORT = int(os.environ.get('PORT', 5000))

token = os.getenv("token", "") #telegram bot token
app_name = os.getenv("RAILWAY_STATIC_URL", "") #app url for webhook

if len(str(app_name)) < 2:
   app_name_heroku = os.getenv("HEROKU_APP_NAME", "")
   if app_name_heroku == "":
      print("please put your app url for webhook in env or disable webhook")
      sys.exit(1)
   app_name = app_name_heroku + ".herokuapp.com"

app_url = "https://" + app_name + "/"
print(app_url)

if len(str(token)) < 5: print("please put your token in env"); sys.exit(1)


keyboard = [
        ["🥺 aww","🐈 cat", "👊 meme"],
        ["🚀space🔭", "🐕 dog", "rick morty🛸"],
        ["🤖 Start the Bot","⁉️ Help"]]


def echo(update: Update, context: CallbackContext):
    r = praw.Reddit('client')
    um = str(update)
    noToDown = 4
    numberToDownload = 0
    if "aww" in um: targetSubreddit = "aww"
    elif "cat" in um: targetSubreddit = "cat"
    elif "dog" in um: targetSubreddit = "dog"
    elif "space" in um: targetSubreddit = "spaceporn"
    elif "meme" in um: targetSubreddit = "memes"
    elif "rick" in um or "morty" in um: targetSubreddit = "rickandmorty"
    else:
      user = update.message.text
      if len(user) == 0:
         update.message.reply_text(text="Specify no. of imgs")
         update.message.reply_text(text="i.e :- \n r/cute 10 \n this command will get 10 imgs from r/cute")
         return

      if re.match("^r/[a-zA-Z]+ [0-9]+$", user):
         print(user)
         subnme, nopost = user.split(" ")
         rsl, subn = subnme.split("r/")
         numberToDownload = int(nopost)
         targetSubreddit = str(subn)
         print(subn)

      elif re.match("^[a-zA-Z]+ [0-9]+$", user):
           print(user)
           subnme, nopost = user.split(" ")
           numberToDownload = int(nopost)
           targetSubreddit = str(subnme)
           print(subnme)

      else:
         update.message.reply_text(text="ERROR !")
         update.message.reply_text(text="PLZ SEND A RIGHT COMMAND \n i.e: \n\n r/cats 10 \n\n OR \n\n cats 10 \n\n this command will get 10 imgs from r/cat")
         return

    def snd(imageUrl, des):
        print(imageUrl)
        context.bot.send_photo(chat_id=update.message.chat_id, photo = imageUrl, caption=des)

    if numberToDownload == 0:
       maxToDownload = noToDown
    else:
       maxToDownload = numberToDownload
    print(maxToDownload)
    for line in range(maxToDownload):
        try:
           l = r.subreddit(targetSubreddit).random()
        except:
           update.message.reply_text(text="SubReddit doesn't exsit")

        try:
           des = l.title
        except:
           print("no title")
           des = "no title"

        try:
           image = l.preview['images'][0]['source']['url']
           snd(image, des)
        except:
           print("not image")
           update.message.reply_text(text="This post doesn't have img")


def start(update: Update, context: CallbackContext):
    username = "@" + update.effective_user.username
    frname = update.effective_user.first_name
    lasname = update.effective_user.last_name
    name = ""

    if username != "None":
       name = username
    elif frname != "None":
       if lasname != "None":
           name = frname + "" + lasname
       else: name = frname
    elif username == "None" and frname == "None":
       name = str(update.message.chat_id)

    update.message.reply_text("""Hey %s!👋 
send me any word (subreddit) and i will scrape images for you :) 
⚠️ REPORT any bugs at @xd2222 or @Pine_Orange ⚠️ """ %name, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

def main():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('🤖 Start the Bot'), start))
    dp.add_handler(MessageHandler(Filters.regex('⁉️ Help'), start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=token) # comment this for local testing
    updater.bot.setWebhook(app_url + token) # comment this for local testing #put your app name for webhook (optional)
    #updater.start_polling() #Un Comment this for local testing
    updater.idle()
    print("ok")
    print("received sigterm")


main()
