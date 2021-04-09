import os

import telebot
from telebot.types import InputMediaPhoto

import config, time
import urllib.request
from datetime import datetime
from urllib.parse import quote, urlsplit, urlunsplit

bot = telebot.TeleBot(config.TOKEN)


def iri_to_uri(iri):
    parts = urlsplit(iri)
    uri = urlunsplit((
        parts.scheme,
        parts.netloc.encode('idna').decode('ascii'),
        quote(parts.path),
        quote(parts.query, '='),
        quote(parts.fragment),
    ))
    return uri

@bot.message_handler(content_types=['text'])
def get_reddit_content(message):
     if "https://www.reddit.com/" in message.text:
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        chat_identity = message.chat.title if message.chat.id < 0 else str(message.chat.id)
        print(current_time + " Chat identity: " + chat_identity)
        url_message = message.text
        start_url = url_message.find("https")
        url = iri_to_uri(url_message[start_url:])
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        try:
            retry_count = 1
            url_response = ...
            while(retry_count<=10):
                try:
                    time.sleep(1)
                    url_response = urllib.request.urlopen(req)
                    break
                except Exception as e:
                    bot.send_message('-556187948', "Chat identity: " + chat_identity + '\n' + "Retry - " + str(retry_count))
                    retry_count += 1
            response_data = url_response.read().decode('utf-8')
            tittle = response_data[response_data.find('<title>') + 7:response_data.find('</title>')]
            tittle = tittle.replace("&#x27;","'").replace("&quot;","")
            if '"type":"image"' in response_data:
                point = response_data.find('"type":"image"')
                start_url = response_data.find("https://", point-200)
                end_url = response_data.find('"', start_url)
                draft_url = response_data[start_url: end_url]
                urllib.request.urlretrieve(draft_url.replace("\\u0026", "&"), "local-filename.jpg")
                foto = open('local-filename.jpg', 'rb')
                os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None, message.id)
                print(current_time + ' Success: "type":"image"')
            elif '"type":"gifvideo"' in response_data:
                arr = response_data.split('"type":"gifvideo"')
                sub = arr[0][-200:]
                draft_url = sub[sub.find('https://'):]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url.replace("\\u0026", "&"))
                print(current_time + ' Success: "type":"gifvideo"')
            elif '.mp4' in response_data:
                arr = response_data.split('.mp4')
                sub = arr[0]
                resolution_arr = arr[1].split('"height":')
                resolution = resolution_arr[1][0:resolution_arr[1].find(',')]
                try:
                    time.sleep(1)
                    urllib.request.urlopen(sub[-39:-2] + resolution + '.mp4')
                    bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + sub[-39:-2] + resolution + '.mp4')
                    print(current_time + ' Success: ".mp4"')
                except Exception as e:
                    bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + sub[-39:-2] + '240.mp4')
                    print(current_time + ' Success: "240.mp4"')
            elif 'https://i.imgur.com/' in response_data:
                draft_url = response_data[response_data.find('https://i.imgur.com/'):]
                url = draft_url[:draft_url.find('"')-4]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url + 'mp4')
                print(current_time + ' Success: "https://i.imgur.com/"')
            elif 'class="_3BxRNDoASi9FbGX01ewiLg' in response_data:
                arr = response_data.split('_3BxRNDoASi9FbGX01ewiLg')
                img_arr = []
                for sub in arr:
                    if 'href="https://preview.redd.it/' in sub:
                        draft_url = sub[sub.find('https://preview.redd.it/'):]
                        url = draft_url[:draft_url.find('"')]
                        image_dimension = url[url.find("?")-3:url.find("?")]
                        urllib.request.urlretrieve(url.replace('amp;', ''), "local-filename."+ image_dimension)
                        foto = open('local-filename.'+ image_dimension, 'rb')
                        if len(img_arr) == 0:
                            img_arr.append(InputMediaPhoto(foto, tittle[0:tittle.find(':')]))
                        else:
                            img_arr.append(InputMediaPhoto(foto))
                        os.remove("local-filename."+ image_dimension)
                bot.send_media_group(message.chat.id, img_arr, None, message.id)
                print(current_time + ' Success: "class="_3BxRNDoASi9FbGX01ewiLg"')
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
                print(current_time + ' Success: "class="_3spkFGVnKMHZ83pDAhW3Mx"')
            elif '<meta property="og:type" content="image" />' in response_data:
                point = response_data.find('property="og:image"')
                start_url = response_data.find("https://", point)
                end_url = response_data.find('"', start_url)
                draft_url = response_data[start_url: end_url]
                urllib.request.urlretrieve(draft_url.replace("amp;", ''), "local-filename.jpg")
                foto = open('local-filename.jpg', 'rb')
                os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None,
                                     message.id)
                print(current_time + ' Success: "property="og:image""')
            else:
                file = open("logs_fails.txt", "a")
                file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                bot.reply_to(message, "image not found")
                print(current_time + ' "image not found"')
        except Exception as e:
            bot.send_message('-556187948', "Chat identity: " + chat_identity + '\n' + 'Error: ' + format(e))
            file = open("logs_errors.txt", "a")
            file.write(current_time + '\n' + str(message.chat.id) + '\n' + url + '\n' + format(e) + '\n' + '\n')
            file.close()
            bot.reply_to(message, "something went wrong")
            print(current_time + ' something went wrong' + '\n' + format(e))

bot.polling(none_stop=True)