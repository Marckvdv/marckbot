# WIP

import io
from PIL import Image
from telegram import InputFile

max_width = 20

def get_char(pixels):
	for y in range(max_width):
		
		for x in range(max_width):

def braille(self):
    def braille_internal(bot, update):
        try:
            message = update.message
            chat = message.chat.id
            reply = message.reply_to_message

            file_id = reply.photo[-1].file_id if reply.photo else reply.document.file_id

            content = self.getFile(file_id)
            image = Image.open(io.BytesIO(content))
			rgb = image.convert("RGB")
			
			width_pixels = image.width // max_width
			height_pixels = image.height // max_width

			for y in range(max_width):
				for x in range(max_width):
					pixels = [[0] * height_pixels for _ in range(max_width)]
					pixels[x][y] = rgb.get_pixel((x, y))

            saved = io.BytesIO()
            image.save(saved, format="JPEG", quality=1)

            self.sendPhoto(converted.getvalue(), chat)
        except AttributeError as e:
            print("error:")
            print(e)

    return braille_internal
