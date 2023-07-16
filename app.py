from flask import Flask, request, render_template
from SpeechRecon import Shazoom

app = Flask(__name__)
# Get your own LyricsGenius Api key
api_key = ''


@app.route('/', methods=["POST", "GET"])
def login_page():
    speech_rec = Shazoom(api_key)
    if request.method == "POST":
        data = speech_rec.get_song_name_from_speech()
        return render_template('results.html', data=data)
    else:
        data = speech_rec.get_three_top_songs()
        return render_template("results.html", data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
