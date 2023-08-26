import os
from pytube import YouTube
from pytube.cli import on_progress
from io import BytesIO
from pytube.exceptions import PytubeError
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    send_file,
)

app = Flask(__name__)


@app.route("/")
def index():
    print("Request for index page received")
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/hello", methods=["POST"])
def hello():
    url = request.form.get("name")
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        buffer = BytesIO()
        audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
    except PytubeError:
        print("error")

    return send_file(
        buffer,
        as_attachment=True,
        attachment_filename=f"{audio.title}.mp3",
        mimetype="audio/mp3",
    )


if __name__ == "__main__":
    app.run()
