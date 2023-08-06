import pychromecast
import asyncio


class Chromecast:
    def __init__(self, kernel):
        pass

class GoogleHome:
    """
        Create a Google home (an host or a devicename is mandatory)
        :param devicename: string : the ip or device name of the Google Home
        :param host: the host of google home
        :param port: the port to contact google home by ip (default is 8009)
        :param ttsbuilder: function: the tts function. This is a function who have two parameter a text string and the lang. This function return an url to download mp3 file
    """
    def __init__(self, devicename=None):
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[devicename])
            
        self.cc = chromecasts[0]

    def say(self, text):
        tts = gTTS(text, lang='en', tld='com.au')
        tts.save('hello.mp3')

    def play(self, url, contenttype = 'audio/mp3'):
        self.cc.wait()
        mc = self.cc.media_controller
        mc.play_media(url, contenttype)
        mc.block_until_active()
        print("played url " + url)

