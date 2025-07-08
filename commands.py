from deep_translator import GoogleTranslator
from pytube import YouTube

def translate(mess="hello", num = 0, lang="ru"):
    if num == 0:
        return GoogleTranslator(source='auto', target=lang).translate(mess)
    elif -1:
        mess = mess.split()
        return GoogleTranslator(source='auto', target=lang).translate(mess[-1])



def download(URL):
    video_url = URL

# Создаем объект YouTube
    yt = YouTube(video_url)

# Выбираем поток (например, самый высокое качество)
    stream = yt.streams.get_highest_resolution()
    return stream

def no_comment():
    return "Хмпф.."