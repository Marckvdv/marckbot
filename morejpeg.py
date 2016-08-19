import io
from PIL import Image
from telegram import InputFile

def morejpeg(self):
    def morejpeg_internal(bot, update):
        try:
            message = update.message
            chat = message.chat.id
            reply = message.reply_to_message

            file_id = reply.photo[-1].file_id if reply.photo else reply.document.file_id

            content = self.getFile(file_id)
            image = Image.open(io.BytesIO(content))
            converted = io.BytesIO()

            image.save(converted, format="JPEG", quality=1)

            self.sendPhoto(converted.getvalue(), chat)
        except AttributeError as e:
            print("error:")
            print(e)

    return morejpeg_internal
