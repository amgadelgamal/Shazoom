import time
import speech_recognition as sr
from lyricsgenius import Genius


class Shazoom:
    def __init__(self, api_key):
        self.api_key = api_key
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def get_speech_from_mic(self):

        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"

        return response

    def get_song_name_from_speech(self):
        print("Starts in 3 seconds....")
        time.sleep(3)

        while True:
            while True:
                print('Speak!')
                guess = self.get_speech_from_mic()
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break

            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
            genius = Genius(self.api_key)
            request = genius.search_all(guess["transcription"].lower())
            top_results = []
            for hit in request['sections'][2]['hits']:
                song_name = hit['result']['title']
                artist = hit['result']['artist_names']
                song_rank = str(len(top_results) + 1)
                song_name_url_version = song_name.replace(" ", "+")
                artist_url_version = artist.replace(" ", "+")
                yt_url = f"https://www.youtube.com/results?search_query={song_name_url_version}+by+{artist_url_version}"
                image = hit['result']['header_image_thumbnail_url']
                top_results.append({'name': song_name,
                                    'artist': artist,
                                    'num': song_rank,
                                    'yt_url': yt_url,
                                    'img': image
                                    })
            if len(top_results) > 0:
                break
        return top_results

    def get_three_top_songs(self):
        genius = Genius(self.api_key)
        request = genius.search_all("to shock you like you won't believe")
        top_results = []
        for hit in request['sections'][2]['hits']:
            song_name = hit['result']['title']
            artist = hit['result']['artist_names']
            song_rank = str(len(top_results) + 1)
            song_name_url_version = song_name.replace(" ", "+")
            artist_url_version = artist.replace(" ", "+")
            yt_url = f"https://www.youtube.com/results?search_query={song_name_url_version}+by+{artist_url_version}"
            image = hit['result']['header_image_thumbnail_url']
            top_results.append({'name': song_name,
                                'artist': artist,
                                'num': song_rank,
                                'yt_url': yt_url,
                                'img': image
                                })

        return top_results
