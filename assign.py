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
            print("Added definition")
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
                if command_name.endswith("@mvdvbot"):
                    command_name = command_name[:-8]
                chat = recv_message.chat.id

                result = self.cursor.execute("SELECT message FROM defines WHERE name=? AND chat=?", (command_name, chat)).fetchone()

                if result != None:
                    msg = jsonpickle.decode(result[0])
                    self.bot.sendMessage(bot, chat, msg)
            except Exception as e:
                print("error:")
                print(e)

        return handle_assign_internal

    def defines(self):
        def defines_internal(bot, update):
            try:
                recv_message = update.message
                chat = recv_message.chat.id

                msg = "Current defines are:\n"

                current = self.cursor.execute("SELECT name FROM defines WHERE chat=?", (chat, )).fetchone()
                while current != None:
                    msg += "- /{}\n".format(current[0])
                    current = self.cursor.fetchone()
                    
                bot.sendMessage(chat, msg)

            except Exception as e:
                print("error:")
                print(e)

        return defines_internal

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
