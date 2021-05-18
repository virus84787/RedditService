import os

import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo

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

def get_current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

@bot.message_handler(content_types=['text'])
def get_reddit_content(message):
     if "https://www.reddit.com/" in message.text:
        chat_identity = message.chat.title if message.chat.id < 0 else str(message.chat.id)
        print('-------------------------' + '\n' + get_current_time() + " Chat identity: " + chat_identity)
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
                    time.sleep(0.1)
                    url_response = urllib.request.urlopen(req)
                    break
                except Exception as e:
                    bot.send_message('-556187948', "Chat identity: " + chat_identity + '\n' + "Retry - " + str(retry_count))
                    retry_count += 1
            response_data = url_response.read().decode('utf-8')
            tittle = response_data[response_data.find('<title>') + 7:response_data.find('</title>')]
            tittle = tittle.replace("&#x27;","'").replace("&quot;","")
            if ('"type":"image"' in response_data) & ('https://i.imgur.com/' not in response_data):
                point = response_data.find('"type":"image"')
                start_url = response_data.find("https://", point-100)
                end_url = response_data.find('"', start_url)
                draft_url = response_data[start_url: end_url]
                time.sleep(0.1)
                urllib.request.urlretrieve(draft_url.replace("\\u0026", "&"), "local-filename.jpg")
                foto = open('local-filename.jpg', 'rb')
                os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None, message.id)
                print(get_current_time() + ' Success: "type":"image"')
            elif '"type":"gifvideo"' in response_data:
                arr = response_data.split('"type":"gifvideo"')
                sub = arr[0][-200:]
                draft_url = sub[sub.find('https://'):]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url.replace("\\u0026", "&"))
                print(get_current_time() + ' Success: "type":"gifvideo"')
            elif ('DASH_96.mp4' in response_data) & ('.mp4,' not in response_data):
                arr = response_data.split('DASH_96.mp4"')
                sub = arr[0]
                resolution_arr = arr[1].split('"height":')
                resolution = resolution_arr[1][0:resolution_arr[1].find(',')]

                try:
                    try:
                        print(get_current_time() + ' Try: "480.mp4" with sound')
                        urllib.request.urlopen(sub[-32:] + 'DASH_480.mp4')
                        url_for_combine = 'https://ds.redditsave.com/download-sd.php?permalink=' + url + '/&video_url=' + sub[
                                                                                                                          -32:] + 'DASH_480.mp4' + '&audio_url=' + sub[
                                                                                                                                                                   -32:] + 'DASH_audio.mp4'
                    except Exception as e:
                        print(get_current_time() + ' Error 480.mp4 with sound: ' + str(e))
                        try:
                            time.sleep(0.01)
                            print(get_current_time() + ' Try: "360.mp4" with sound')
                            urllib.request.urlopen(sub[-32:] + 'DASH_360.mp4')
                            url_for_combine = 'https://ds.redditsave.com/download-sd.php?permalink=' + url + '/&video_url=' + sub[
                                                                                                                              -32:] + 'DASH_360.mp4' + '&audio_url=' + sub[
                                                                                                                                                                       -32:] + 'DASH_audio.mp4'
                        except Exception as e:
                            print(get_current_time() + ' Error 360.mp4 with sound: ' + str(e))
                            print(get_current_time() + ' Try: "240.mp4" with sound')
                            url_for_combine = 'https://ds.redditsave.com/download-sd.php?permalink=' + url + '/&video_url=' + sub[
                                                                                                                              -32:] + 'DASH_240.mp4' + '&audio_url=' + sub[
                                                                                                                                                                       -32:] + 'DASH_audio.mp4'
                    urllib.request.urlretrieve(url_for_combine, "local-filename.mp4")
                    video = open('local-filename.mp4', 'rb')
                    os.remove("local-filename.mp4")
                    bot.send_media_group(message.chat.id, [InputMediaVideo(video, None, tittle[0:tittle.find(':')])],
                                         None, message.id)
                    print(get_current_time() + ' Success: ".mp4" with sound')
                except Exception as e:
                    print(get_current_time() + ' Error 240.mp4 with sound: ' + str(e))
                    try:
                        urllib.request.urlopen(sub[-32:] + 'DASH_' + resolution + '.mp4')
                        bot.reply_to(message,
                                     tittle[0:tittle.find(':')] + '\n' + sub[-32:] + 'DASH_' + resolution + '.mp4')
                        print(get_current_time() + ' Success: "resolution.mp4"')
                    except Exception as e:
                        print(get_current_time() + ' Error resolution.mp4 without sound: ' + str(e))
                        urllib.request.urlopen(sub[-32:] + 'DASH_240.mp4')
                        bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + sub[-32:] + 'DASH_240.mp4')
                        print(get_current_time() + ' Success: "240.mp4"')

            elif 'https://i.imgur.com/' in response_data:
                draft_url = response_data[response_data.find('https://i.imgur.com/'):]
                url = draft_url[:draft_url.find('"')-4]
                try:
                    urllib.request.urlopen(url + 'mp4')
                    bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url + 'mp4')
                except Exception as e:
                    bot.reply_to(message, url)
                print(get_current_time() + ' Success: "https://i.imgur.com/"')
            elif 'https://a.kyouko.se/' in response_data:
                draft_url = response_data[response_data.find('https://a.kyouko.se/'):]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url)
                print(get_current_time() + ' Success: "https://a.kyouko.se/"')
            elif 'https://gfycat.com/' in response_data:
                draft_url = response_data[response_data.find('https://gfycat.com/'):]
                inner_url = draft_url[:draft_url.find('"')]
                inner_url_response = urllib.request.urlopen(inner_url)
                inner_response_data = inner_url_response.read().decode('utf-8')
                draft_url = inner_response_data[inner_response_data.find("og:video:secure_url")+30:]
                url = draft_url[:draft_url.find('"')]
                bot.reply_to(message, tittle[0:tittle.find(':')] + '\n' + url)
                print(get_current_time() + ' Success: "https://gfycat.com/"')
            elif 'class="_3BxRNDoASi9FbGX01ewiLg' in response_data:
                arr = response_data.split('_3BxRNDoASi9FbGX01ewiLg')
                img_arr = []
                for sub in arr:
                    if 'href="https://preview.redd.it/' in sub:
                        draft_url = sub[sub.find('https://preview.redd.it/'):]
                        url = draft_url[:draft_url.find('"')]
                        image_dimension = url[url.find("?")-3:url.find("?")]
                        time.sleep(0.1)
                        urllib.request.urlretrieve(url.replace('amp;', ''), "local-filename."+ image_dimension)
                        foto = open('local-filename.'+ image_dimension, 'rb')
                        if len(img_arr) == 0:
                            img_arr.append(InputMediaPhoto(foto, tittle[0:tittle.find(':')]))
                        else:
                            img_arr.append(InputMediaPhoto(foto))
                        os.remove("local-filename."+ image_dimension)
                bot.send_media_group(message.chat.id, img_arr, None, message.id)
                print(get_current_time() + ' Success: "class="_3BxRNDoASi9FbGX01ewiLg"')
            elif 'class="_3spkFGVnKMHZ83pDAhW3Mx' in response_data:
                arr = response_data.split('class="_3spkFGVnKMHZ83pDAhW3Mx')
                img_arr = []
                for sub in arr:
                    if 'href="https://preview.redd.it/' in sub:
                        draft_url = sub[sub.find('https://preview.redd.it/'):]
                        url = draft_url[:draft_url.find('"')]
                        time.sleep(0.1)
                        urllib.request.urlretrieve(url.replace('amp;', ''), "local-filename.jpg")
                        foto = open('local-filename.jpg', 'rb')
                        if len(img_arr) == 0:
                            img_arr.append(InputMediaPhoto(foto, tittle[0:tittle.find(':')]))
                        else:
                            img_arr.append(InputMediaPhoto(foto))
                        os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, img_arr, None, message.id)
                print(get_current_time() + ' Success: "class="_3spkFGVnKMHZ83pDAhW3Mx"')
            elif '<meta property="og:type" content="image" />' in response_data:
                point = response_data.find('property="og:image"')
                start_url = response_data.find("https://", point)
                end_url = response_data.find('"', start_url)
                draft_url = response_data[start_url: end_url]
                time.sleep(0.1)
                urllib.request.urlretrieve(draft_url.replace("amp;", ''), "local-filename.jpg")
                foto = open('local-filename.jpg', 'rb')
                os.remove("local-filename.jpg")
                bot.send_media_group(message.chat.id, [InputMediaPhoto(foto, tittle[0:tittle.find(':')])], None,
                                     message.id)
                print(get_current_time() + ' Success: "property="og:image""')
            else:
                file = open("logs_fails.txt", "a")
                file.write(get_current_time() + '\n' + str(message.chat.id) + '\n' + url + '\n' + '\n')
                file.close()
                bot.reply_to(message, "image not found")
                print(get_current_time() + ' "image not found"')
        except Exception as e:
            bot.send_message('-556187948', "Chat identity: " + chat_identity + '\n' + 'Error: ' + str(e))
            file = open("logs_errors.txt", "a")
            file.write(get_current_time() + '\n' + str(message.chat.id) + '\n' + url + '\n' + str(e) + '\n' + '\n')
            file.close()
            bot.reply_to(message, "something went wrong")
            print(get_current_time() + ' something went wrong' + '\n' + str(e))

bot.polling(none_stop=True)