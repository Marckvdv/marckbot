import regex as re

def substitute(bot, update):
    try:
        message = update.message
        parsed = re.search('s/(.+)/(.*)/', message.text)

        match = parsed.group(1)
        replace = parsed.group(2)
        print("match: {}\nreplace: {}".format(match, replace))

        reply = message.reply_to_message
        processed_message = re.sub(match, replace, reply.text)

        chat = update.message.chat.id

        bot.sendMessage(chat, processed_message)
    except AttributeError as e:
        print("error:")
        print(e)
