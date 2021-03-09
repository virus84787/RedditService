import telebot
import config
import urllib.request
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def get_reddit_content(message):
    if "https://www.reddit.com/" in message.text:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        url_message = message.text
        start_url = url_message.find("https")
        url = url_message[start_url:]
        try:
            url_response = urllib.request.urlopen(url)
            response_data = url_response.read().decode('utf-8')
            if '"type":"image"' in response_data:
                file = open("logs_images.txt", "a")
                file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                arr = response_data.split('"type":"image"')
                sub = arr[0]
                bot.reply_to(message, sub[-37:-2])
            elif '.mp4' in response_data:
                file = open("logs_videos.txt", "a")
                file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                arr = response_data.split('.mp4')
                sub = arr[0]
                resolution_arr = arr[1].split('"height":')
                resolution = resolution_arr[1][0:resolution_arr[1].find(',')]
                bot.reply_to(message, sub[-39:-2] + resolution + '.mp4')
            else:
                file = open("logs_fails.txt", "a")
                file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                bot.reply_to(message, "image not found")
        except Exception as e:
            file = open("logs_errors.txt", "a")
            file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + format(e) + '\n' + '\n')
            file.close()
            bot.reply_to(message, "something went wrong")


bot.polling(none_stop=True)