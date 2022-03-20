import telebot
import pathlib
import subprocess
import os

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN, parse_mode=None)
filepath = os.getcwd()
mp3_path = filepath + "/audio.mp3"
ogg_path = filepath + "/audio.ogg"

# info
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Отправьте mp3 файл, чтобы конвертировать его в голосовое сообщение.")
    
# handle mp3 document
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    try:
        # download mp3 file
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # save audio
        with open(mp3_path, "wb") as f:
            f.write(downloaded_file)
            
        # convert audio to ogg with opus codec
        subprocess.run(["ffmpeg", '-i', mp3_path, '-acodec', 'libopus', "-b:a", "32k", ogg_path, '-y'])
        
        # read ogg file
        with open(ogg_path, 'rb') as f:
            data = f.read()

        # send audio as voice message
        bot.send_voice(message.chat.id, data)
    except Exception as e:
        # log error if convert was failed
        print(e)
        bot.send_message(message.chat.id, "Ошибка обработки аудио")
        
bot.infinity_polling()