from telegram.ext import Updater
from telegram.ext import CommandHandler, RegexHandler
import io
import requests
import logging
import signal

import substitute
import morejpeg
import assign as myassign

class Bot:
    
    def __init__(self):
        token_file = open("token.txt")
        self.token = token_file.read().strip()

        self.api_url = "https://api.telegram.org"
        self.bot_url = self.api_url + "/bot" + self.token

        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        self.assign_handler = myassign.AssignHandler(self)

        self.assign_handler.importDefinitions()
        signal.signal(signal.SIGINT, self.stop)

        self.dispatcher.add_handler(CommandHandler('assign', self.assign_handler.assign()))
        self.dispatcher.add_handler(CommandHandler('unassign', self.assign_handler.unassign()))
        self.dispatcher.add_handler(CommandHandler('defines', self.assign_handler.defines()))
        self.dispatcher.add_handler(CommandHandler('morejpeg', morejpeg.morejpeg(self)))
        self.dispatcher.add_handler(RegexHandler('s/.+/.*/', substitute.substitute))
        self.dispatcher.add_handler(RegexHandler('/.+', self.assign_handler.handle_assign()))

        self.updater.start_polling()

    def getFile(self, file_id):
        url = self.bot_url + "/getFile"
        info = requests.post(url, data={ "file_id": file_id }).json()
        path = info["result"]["file_path"]

        url = self.api_url + "/file/bot" + self.token + "/" + path
        return requests.get(url).content

    def sendPhoto(self, content, chat_id):
        url = self.bot_url + "/sendPhoto"
        data = {"chat_id": chat_id}
        files = {"photo": ("a.jpg", content)}
        response = requests.post(url, data = data, files = files)

    def sendVoice(self, content, chat_id):
        url = self.bot_url + "/sendVoice"
        data = {"chat_id": chat_id}
        files = {"voice": ("a.mp3", content)}
        response = requests.post(url, data = data, files = files)

    def sendMessage(self, bot, chat, message):
        if message.text:
            bot.sendMessage(chat, message.text)
        elif message.audio:
            bot.sendAudio(chat, message.audio.file_id)
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
            elif message.voice:
                bot.sendVoice(chat, message.voice.file_id, caption=caption)

    def stop(self, signal, frame):
        print("HALTING - Recieved SIGINT")

        self.assign_handler.exportDefinitions()
        self.updater.stop()

bot = Bot()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
