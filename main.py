import os

import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo

import config, time
import urllib.request
from datetime import datetime
from urllib.parse import quote, urlsplit, urlunsplit

bot = telebot.TeleBot(config.TOKEN)
me_chat_id = config.ME_CHAT_ID
rusik_chat_id = config.RUSIK_CHAT_ID
max_chat_id = config.MAX_CHAT_ID
dev_chat_id = config.DEV_CHAT_ID



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


def get_current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


@bot.message_handler(content_types=['text'])
def get_reddit_content(message):
    if "https://www.reddit.com/" in message.text:
        chat_identity = message.chat.title if message.chat.id < 0 else str(message.chat.id)
        chat_identity = "!!!ME!!!" if chat_identity == me_chat_id else chat_identity
        chat_identity = "!!!RUSIK!!!" if chat_identity == rusik_chat_id else chat_identity
        chat_identity = "!!!MAX!!!" if chat_identity == max_chat_id else chat_identity

        try:
            file = open("id.txt", "r")
        except Exception as e:
            file = open("id.txt", "w")
            file.close()
            file = open("id.txt", "r")
        s = file.read()
        id = int(s) if s != '' else 1
        file.close()
        file = open("id.txt", "w")
        file.write(str(id + 1))
        file.close()
        print('-------------------------' + '\n' + get_current_time() + " id: " + str(
            id) + " Chat identity: " + chat_identity)
        url_message = message.text
        start_url = url_message.find("https")
        url = iri_to_uri(url_message[start_url:])
        print(get_current_time() + " id: " + str(id) + " URL: " + url)
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
            while (retry_count <= 10):
                try:
                    time.sleep(0.1)
                    url_response = urllib.request.urlopen(req)
                    break
                except Exception as e:
                    bot.send_message('-556187948',
                                     "Chat identity: " + chat_identity + '\n' + "Retry - " + str(retry_count))
                    retry_count += 1
            response_data = url_response.read().decode('utf-8')
            tittle = response_data[response_data.find('<title>') + 7:response_data.find('</title>')]
            tittle = tittle.replace("&#x27;", "'").replace("&quot;", "")
            if '"type":"image"' in response_data:
                point = response_data.find('"type":"image"')
                start_url = response_data.find("https://", point - 100)
                end_url = response_data.find('"', start_url)
                draft_url = response_data[start_url: end_url]
                time.sleep(0.1)
                urllib.request.urlretrieve(draft_url.replace("\\u0026", "&"), str(id) + ".jpg")
                foto = open(str(id) + '.jpg', 'rb')
                os.remove(str(id) + ".jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None,
                                     message.id)
                print(get_current_time() + " id: " + str(id) + ' Success: "type":"image"')
            elif ('.mp4' in response_data) & ('.mp4,' not in response_data):
                arr = response_data.split('DASH_96.mp4"')
                sub = arr[0]
                resolution_arr = arr[1].split('"height":')
                resolution = resolution_arr[1][0:resolution_arr[1].find(',')]

                try:
                    try:
                        print(get_current_time() + " id: " + str(id) + ' Try: "480.mp4" with sound')
                        urllib.request.urlopen(sub[-32:] + 'DASH_480.mp4')
                        url_for_combine = 'https://ds.redditsave.com/download-sd.php?permalink=' + url + '/&video_url=' + sub[
                                                                                                                          -32:] + 'DASH_480.mp4' + '&audio_url=' + sub[
                                                                                                                                                                   -32:] + 'DASH_audio.mp4'
                    except Exception as e:
                        print(get_current_time() + " id: " + str(id) + ' Error 480.mp4 with sound: ' + str(e))
                        try:
                            time.sleep(0.01)
                            print(get_current_time() + " id: " + str(id) + ' Try: "360.mp4" with sound')
                            urllib.request.urlopen(sub[-32:] + 'DASH_360.mp4')
                            url_for_combine = 'https://ds.redditsave.com/download-sd.php?permalink=' + url + '/&video_url=' + sub[
                                                                                                                              -32:] + 'DASH_360.mp4' + '&audio_url=' + sub[
                                                                                                                                                                       -32:] + 'DASH_audio.mp4'
                        except Exception as e:
                            print(get_current_time() + " id: " + str(id) + ' Error 360.mp4 with sound: ' + str(e))
                            print(get_current_time() + " id: " + str(id) + ' Try: "240.mp4" with sound')
                            url_for_combine = 'https://ds.redditsave.com/download-sd.php?permalink=' + url + '/&video_url=' + sub[
                                                                                                                              -32:] + 'DASH_240.mp4' + '&audio_url=' + sub[
                                                                                                                                                                       -32:] + 'DASH_audio.mp4'
                    urllib.request.urlretrieve(url_for_combine, str(id) + ".mp4")
                    video = open(str(id) + '.mp4', 'rb')
                    os.remove(str(id) + ".mp4")
                    bot.send_media_group(message.chat.id, [InputMediaVideo(video, None, tittle[0:tittle.find(':')])],
                                         None, message.id)
                    print(get_current_time() + " id: " + str(id) + ' Success: ".mp4" with sound')
                except Exception as e:
                    print(get_current_time() + " id: " + str(id) + ' Error 240.mp4 with sound: ' + str(e))
                    try:
                        urllib.request.urlopen(sub[-32:] + 'DASH_' + resolution + '.mp4')
                        bot.reply_to(message,
                                     tittle[0:tittle.find(':')] + '\n' + sub[-32:] + 'DASH_' + resolution + '.mp4')
                        print(get_current_time() + " id: " + str(id) + ' Success: "resolution.mp4"')
                    except Exception as e:
                        print(get_current_time() + " id: " + str(id) + ' Error resolution.mp4 without sound: ' + str(e))
                        urllib.request.urlopen(sub[-32:] + 'DASH_240.mp4')
                        bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + sub[-32:] + 'DASH_240.mp4')
                        print(get_current_time() + " id: " + str(id) + ' Success: "240.mp4"')
            elif 'https://gfycat.com/' in response_data:
                draft_url = response_data[response_data.find('https://gfycat.com/'):]
                inner_url = draft_url[:draft_url.find('"')]
                inner_url_response = urllib.request.urlopen(inner_url)
                inner_response_data = inner_url_response.read().decode('utf-8')
                draft_url = inner_response_data[inner_response_data.find("og:video:secure_url") + 30:]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url)
                print(get_current_time() + " id: " + str(id) + ' Success: "https://gfycat.com/"')
            elif 'https://clips.twitch.tv' in response_data:
                draft_url = response_data[response_data.find('https://clips.twitch.tv'):]
                inner_url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + inner_url)
                print(get_current_time() + " id: " + str(id) + ' Success: "https://clips.twitch.tv"')
            elif '"type":"gifvideo"' in response_data:
                arr = response_data.split('"type":"gifvideo"')
                sub = arr[0][-200:]
                draft_url = sub[sub.find('https://'):]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url.replace("\\u0026", "&"))
                print(get_current_time() + " id: " + str(id) + ' Success: "type":"gifvideo"')
            elif 'class="_3BxRNDoASi9FbGX01ewiLg' in response_data or 'class="_3spkFGVnKMHZ83pDAhW3Mx' in response_data or 'class="_35oEP5zLnhKEbj5BlkTBUA' in response_data:
                separator = ''
                if  'class="_3BxRNDoASi9FbGX01ewiLg' in response_data:
                    separator = 'class="_3BxRNDoASi9FbGX01ewiLg'
                elif 'class="_3spkFGVnKMHZ83pDAhW3Mx' in response_data:
                    separator = 'class="_3spkFGVnKMHZ83pDAhW3Mx'
                elif 'class="_35oEP5zLnhKEbj5BlkTBUA' in response_data:
                    separator = 'class="_35oEP5zLnhKEbj5BlkTBUA'
                else:
                    print(get_current_time() + " id: " + str(id) + ' Unsupport multimedia separator')
                arr = response_data.split(separator)
                img_arr = []
                img_count = 0
                part_string = ""
                part_count = 0
                for sub in arr:
                    if 'href="https://preview.redd.it/' in sub:
                        draft_url = sub[sub.find('https://preview.redd.it/'):]
                        url = draft_url[:draft_url.find('"')]
                        image_dimension = url[url.find("?") - 3:url.find("?")]
                        time.sleep(0.1)
                        urllib.request.urlretrieve(url.replace('amp;', ''), str(id) + "." + image_dimension)
                        foto = open(str(id) + '.' + image_dimension, 'rb')
                        if len(img_arr) == 0:
                            if len(arr) > 21:
                                part_count += 1
                                part_string = " (Part " + str(part_count) + ")"
                            img_arr.append(InputMediaPhoto(foto, tittle[0:tittle.find(':')] + part_string))
                        else:
                            img_arr.append(InputMediaPhoto(foto))
                        os.remove(str(id) + "." + image_dimension)
                        img_count += 1
                        if img_count == 10:
                            bot.send_media_group(message.chat.id, img_arr, None, message.id)
                            img_arr = []
                            img_count = 0
                if img_count % 10 != 0:
                    bot.send_media_group(message.chat.id, img_arr, None, message.id)
                print(get_current_time() + " id: " + str(id) + ' Success: ' + separator)
            elif '<meta property="og:type" content="image" />' in response_data:
                point = response_data.find('property="og:image"')
                start_url = response_data.find("https://", point)
                end_url = response_data.find('"', start_url)
                draft_url = response_data[start_url: end_url]
                time.sleep(0.1)
                urllib.request.urlretrieve(draft_url.replace("amp;", ''), str(id) + ".jpg")
                foto = open(str(id) + '.jpg', 'rb')
                os.remove(str(id) + ".jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None,
                                     message.id)
                print(get_current_time() + " id: " + str(id) + ' Success: "property="og:image""')
            elif 'https://streamwo.com/' in response_data:
                draft_url = response_data[response_data.find('https://streamwo.com/'):]
                inner_url = draft_url[:draft_url.find('"')]
                req = urllib.request.Request(
                    inner_url,
                    data=None,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
                )
                inner_url_response = urllib.request.urlopen(req)
                inner_response_data = inner_url_response.read().decode('utf-8')
                draft_url = inner_response_data[inner_response_data.find("source src=") + 12:]
                url = draft_url[:draft_url.find('"')]
                urllib.request.urlretrieve(url, str(id) + ".mp4")
                video = open(str(id) + '.mp4', 'rb')
                os.remove(str(id) + ".mp4")
                bot.send_media_group(message.chat.id, [InputMediaVideo(video, None, tittle[0:tittle.find(':')])],
                                     None, message.id)
                print(get_current_time() + " id: " + str(id) + ' Success: "https://streamwo.com/')
            elif 'https://streamable.com/' in response_data:
                draft_url = response_data[response_data.find('https://streamable.com/'):]
                inner_url = draft_url[:draft_url.find('"')]
                inner_url_response = urllib.request.urlopen(inner_url)
                inner_response_data = inner_url_response.read().decode('utf-8')
                draft_url = inner_response_data[inner_response_data.find("og:video:secure_url") + 30:]
                url = draft_url[:draft_url.find('"')]
                urllib.request.urlretrieve(url, str(id) + ".mp4")
                video = open(str(id) + '.mp4', 'rb')
                os.remove(str(id) + ".mp4")
                bot.send_media_group(message.chat.id, [InputMediaVideo(video, None, tittle[0:tittle.find(':')])],
                                     None, message.id)
                print(get_current_time() + " id: " + str(id) + ' Success: "https://streamable.com/')
            elif 'youtu' in response_data:
                draft_url = response_data[response_data.find('https://www.youtu'):]
                if draft_url == ' ':
                    draft_url = response_data[response_data.find('https://youtu'):]
                if draft_url == ' ':
                    draft_url = response_data[response_data.find('https://m.youtu'):]
                inner_url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + inner_url.replace('amp;', ''))
                print(get_current_time() + " id: " + str(id) + ' Success: YouTube')
            elif 'https://i.imgur.com/' in response_data:
                draft_url = response_data[response_data.find('https://i.imgur.com/'):]
                url = draft_url[:draft_url.find('"') - 4]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url + 'mp4')
                print(get_current_time() + " id: " + str(id) + ' Success: "https://i.imgur.com/"')
            else:
                file = open("logs_fails.txt", "a")
                file.write(
                    get_current_time() + " id: " + str(id) + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                bot.reply_to(message, "Supported content for extract not found")
                print(get_current_time() + " id: " + str(id) + ' "Supported content for extract not found"')
        except Exception as e:
            bot.send_message(dev_chat_id, "Chat identity: " + chat_identity + '\n' + 'Error: ' + str(e))
            file = open("logs_errors.txt", "a")
            file.write(get_current_time() + " id: " + str(id) + '\n' + str(message.chat.id) + '\n' + url + '\n' + str(
                e) + '\n' + '\n')
            file.close()
            bot.reply_to(message, "something went wrong")
            print(get_current_time() + " id: " + str(id) + ' something went wrong' + '\n' + str(e))


bot.polling(none_stop=True)