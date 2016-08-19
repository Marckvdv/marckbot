from telegram.ext import CommandHandler
import jsonpickle
import json

class AssignHandler:
    definitions = {}

    def __init__(self, bot):
        self.bot = bot

    def assign(self):
        def assign_interal(bot, update):
            try:
                message = update.message
                words = message.text.split()
                if len(words) != 2:
                    return

                command_name = message.text.split()[1]

                reply = message.reply_to_message
                chat = update.message.chat.id

                self.addCommandAndDefinition(command_name, reply, chat)
            except AttributeError as e:
                print("error:")
                print(e)

        return assign_interal

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
        self.bot.dispatcher.add_handler(CommandHandler(name, function))

    def getSendFunction(self, name):
        def function(bot, update):
            message = self.getDefinitionMessage(name, update.message.chat.id)
            if message != None:
                self.bot.sendMessage(bot, update.message.chat.id, message)

        return function

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
