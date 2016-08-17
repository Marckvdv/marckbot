from telegram.ext import Updater
from telegram.ext import CommandHandler, RegexHandler
import logging
import signal
import jsonpickle
import json
import re

class Bot:
    definitions = {}
    token = "256252332:AAFQwflc2WtEzfMxGpnINJwlJIwzsv8oRSg"
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    def __init__(self):
        self.importDefinitions()

        signal.signal(signal.SIGINT, self.stop)

        self.dispatcher.add_handler(CommandHandler('assign', self.assign))
        self.dispatcher.add_handler(RegexHandler('s/.+/.*/', self.substitute))
        self.updater.start_polling()

    def substitute(self, bot, update):
        try:
            message = update.message
            parsed = re.search('s/(.+)/(.*)/', message.text)

            match = parsed.group(1)
            replace = parsed.group(2)
            reply = message.reply_to_message
            processed_message = re.sub(match, replace, reply.text)

            chat = update.message.chat.id

            bot.sendMessage(chat, processed_message)
        except AttributeError as e:
            print("error:")
            print(e)

    def assign(self, bot, update):
        try:
            message = update.message

            reply = message.reply_to_message
            name = message.text.split()[1]
            chat = update.message.chat.id

            self.addCommandAndDefinition(name, reply, chat)
        except AttributeError as e:
            print("error:")
            print(e)

    def addDefinition(self, name, message, chat):
        if self.definitions.get(name) == None:
            self.definitions[name] = {}
        self.definitions[name][chat] = message

    def getDefinitionMessage(self, name, chat):
        nameDefinition = self.definitions.get(name)
        if nameDefinition != None:
            return nameDefinition.get(chat)
        else:
            return None

    def addCommandAndDefinition(self, name, message, chat):
        self.addDefinition(name, message, chat)
        self.addCommand(name)

    def addCommand(self, name):
        if self.definitions.get(name) == None: return

        function = self.getSendFunction(name)
        self.dispatcher.add_handler(CommandHandler(name, function))

    def getSendFunction(self, name):
        def function(bot, update):
            message = self.getDefinitionMessage(name, update.message.chat.id)
            if message != None:
                Bot.sendMessage(bot, update.message.chat.id, message)

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

            for name, chats in self.definitions.items():
                for chat, message in chats.items():
                    self.addCommand(name)

        except FileNotFoundError:
            print("no previous definitions found, starting anew")
        except json.JSONDecodeError:
            print("failed parsing json, starting anew")

bot = Bot()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
