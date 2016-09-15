import sqlite3
import jsonpickle
import re

db_path = 'defines.db'

class AssignHandler:
    def __init__(self, bot):
        self.bot = bot

    def assign(self):
        def assign_interal(bot, update):
            try:
                message = update.message
                words = message.text.split()
                if len(words) != 2:
                    return

                command_name = message.text.split()[1].lower()

                reply = message.reply_to_message
                chat = update.message.chat.id

                self.addDefinition(command_name, reply, chat)
            except AttributeError as e:
                print("error:")
                print(e)

        return assign_interal

    def addDefinition(self, name, message, chat):
        encoded_message = jsonpickle.encode(message)
        
        self.cursor.execute("SELECT chat, name FROM defines WHERE name=? AND chat=?", (name, chat))
        if self.cursor.fetchone() == None:
            self.cursor.execute("INSERT INTO defines (name, chat, message, active) VALUES (?, ?, ?, ?)", (name, chat, encoded_message, 1))
            self.db.commit()

    def removeDefinition(self, name, chat):
        print("NAME: {}, CHAT: {}".format(name, chat))
        self.cursor.execute("DELETE FROM defines WHERE name=? AND chat=?", (name, chat))
        self.db.commit()

    def getDefinitionMessage(self, name, chat):
        self.cursor.execute("SELECT message FROM defines WHERE name=? AND chat=?", (name, chat))
        message = self.cursor.fetchone()[0]

        return jsonpickle.decode(message)

    def getSendFunction(self, name):
        def function(bot, update):
            message = self.getDefinitionMessage(name, update.message.chat.id)
            if message != None:
                self.bot.sendMessage(bot, update.message.chat.id, message)

        return function

    def exportDefinitions(self):
        self.db.close()

    def importDefinitions(self):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.db.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS defines (name text, chat text, message text, active integer)")

        self.db.commit()

    def handle_assign(self):
        def handle_assign_internal(bot, update):
            try:
                recv_message = update.message
                command_name = re.search('/(.+)', recv_message.text).group(1).lower()
                chat = recv_message.chat.id

                result = self.cursor.execute("SELECT message FROM defines WHERE name=? AND chat=?", (command_name, chat)).fetchone()

                if result != None:
                    self.bot.sendMessage(bot, chat, jsonpickle.decode(result[0]))
            except AttributeError as e:
                print("error:")
                print(e)
            

        return handle_assign_internal

    def unassign(self):
        def unassign_interal(bot, update):
            try:
                message = update.message
                words = message.text.split()
                if len(words) != 2:
                    return

                command_name = message.text.split()[1].lower()

                reply = message.reply_to_message
                chat = update.message.chat.id

                self.removeDefinition(command_name, chat)
            except AttributeError as e:
                print("error:")
                print(e)

        return unassign_interal
