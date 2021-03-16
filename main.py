import os

import telebot
from telebot.types import InputMediaPhoto

import config
import urllib.request
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def get_reddit_content(message):
    if "https://www.reddit.com/" in message.text:
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        url_message = message.text
        start_url = url_message.find("https")
        url = url_message[start_url:]
        try:
            try:
                url_response = urllib.request.urlopen(url)
            except Exception as e:
                try:
                    url_response = urllib.request.urlopen(url)
                except Exception as e:
                    url_response = urllib.request.urlopen(url)
            response_data = url_response.read().decode('utf-8')
            tittle = response_data[response_data.find('<title>') + 7:response_data.find('</title>')]
            tittle = tittle.replace("&#x27;","'")
            if '"type":"image"' in response_data:
                file = open("logs_images.txt", "a")
                file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                arr = response_data.split('"type":"image"')
                sub = arr[0]
                urllib.request.urlretrieve(sub[-37:-2], "local-filename.jpg")
                foto = open('local-filename.jpg', 'rb')
                os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None, message.id)
                # bot.reply_to(message, sub[-37:-2])
            elif '"type":"gifvideo"' in response_data:
                arr = response_data.split('"type":"gifvideo"')
                sub = arr[0][-200:]
                draft_url = sub[sub.find('https://preview.redd.it/'):]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, url.replace("\\u0026", "&"))
            elif '.mp4' in response_data:
                file = open("logs_videos.txt", "a")
                file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                arr = response_data.split('.mp4')
                sub = arr[0]
                resolution_arr = arr[1].split('"height":')
                resolution = resolution_arr[1][0:resolution_arr[1].find(',')]
                try:
                    urllib.request.urlopen(sub[-39:-2] + resolution + '.mp4')
                    bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + sub[-39:-2] + resolution + '.mp4')
                except Exception as e:
                    bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + sub[-39:-2] + '240.mp4')
            elif 'https://i.imgur.com/' in response_data:
                draft_url = response_data[response_data.find('https://i.imgur.com/'):]
                url = draft_url[:draft_url.find('"')-4]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url + 'mp4')
            elif 'class="_3BxRNDoASi9FbGX01ewiLg' in response_data:
                arr = response_data.split('_3BxRNDoASi9FbGX01ewiLg')
                img_arr = []
                for sub in arr:
                    if 'href="https://preview.redd.it/' in sub:
                        draft_url = sub[sub.find('https://preview.redd.it/'):]
                        url = draft_url[:draft_url.find('"')]
                        urllib.request.urlretrieve(url.replace('amp;', ''), "local-filename.jpg")
                        foto = open('local-filename.jpg', 'rb')
                        if len(img_arr) == 0:
                            img_arr.append(InputMediaPhoto(foto, tittle[0:tittle.find(':')]))
                        else:
                            img_arr.append(InputMediaPhoto(foto))
                        os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, img_arr, None, message.id)
            elif 'class="_3spkFGVnKMHZ83pDAhW3Mx' in response_data:
                arr = response_data.split('class="_3spkFGVnKMHZ83pDAhW3Mx')
                img_arr = []
                for sub in arr:
                    if 'href="https://preview.redd.it/' in sub:
                        draft_url = sub[sub.find('https://preview.redd.it/'):]
                        url = draft_url[:draft_url.find('"')]
                        urllib.request.urlretrieve(url.replace('amp;', ''), "local-filename.jpg")
                        foto = open('local-filename.jpg', 'rb')
                        if len(img_arr) == 0:
                            img_arr.append(InputMediaPhoto(foto, tittle[0:tittle.find(':')]))
                        else:
                            img_arr.append(InputMediaPhoto(foto))
                        os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, img_arr, None, message.id)
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