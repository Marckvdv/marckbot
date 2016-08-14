from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import signal
import jsonpickle
import json

class Bot:
    definitions = []
    token = "256252332:AAFQwflc2WtEzfMxGpnINJwlJIwzsv8oRSg"
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    def __init__(self):
        self.importDefinitions()

        signal.signal(signal.SIGINT, self.stop)

        self.dispatcher.add_handler(CommandHandler('assign', self.assign))
        self.updater.start_polling()

    def assign(self, bot, update):
        print("assigning")
        try:
            message = update.message

            reply = message.reply_to_message
            name = message.text.split()[1]
            chat = update.message.chat.id

            self.addDefinition(name, reply, chat)
            self.addCommand(name, reply, chat)
        except AttributeError as e:
            print("error:")
            print(e)

    def addDefinition(self, name, message, chat):
        self.definitions.append({'name': name, 'message': message})

    def addCommand(self, name, message, chat):
        function = self.getSendFunction(chat, message)
        self.dispatcher.add_handler(CommandHandler(name, function))

    def getSendFunction(self, chat, message):
        def function(bot, update):
            print("triggered, ({} == {} ?)".format(repr(chat), repr(update.message.chat.id)))
            if chat == update.message.chat.id:
                print("and correct chat")
                Bot.sendMessage(bot, chat, message)

        return function

    def sendMessage(bot, chat, message):
        if message.text:
            bot.sendMessage(chat, message.text)
        elif message.audio:
            bot.sendAudio(chat, message.audio.file_id)
        elif message.sticker:
            bot.sendSticker(chat, message.sticker.file_id)
        elif message.sticker:
            bot.sendSticker(chat, message.sticker.file_id)
        else:
            caption = message.caption
            if message.document:
                bot.sendDocument(chat, message.document.file_id, caption=caption)
            elif message.photo:
                bot.sendPhoto(chat, message.photo[0].file_id, caption=caption)
            elif message.video:
                bot.sendVideo(chat, message.video.file_id, caption=caption)

    def stop(self, signal, frame):
        print("HALTING - Recieved SIGINT")

        self.exportDefinitions()
        self.updater.stop()

    def exportDefinitions(self):
        f = open('defs.json', 'w')
        f.write(jsonpickle.encode(self.definitions))

    def importDefinitions(self):
        try:
            f = open('defs.json', 'r')
            self.definitions = jsonpickle.decode(f.read())

            for definition in self.definitions:
                name = definition['name']
                message = definition['message']

                self.addCommand(name, message, message.chat.id)

        except FileNotFoundError:
            print("no previous definitions found, starting anew")
        except json.JSONDecodeError:
            print("failed parsing json, starting anew")

bot = Bot()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
