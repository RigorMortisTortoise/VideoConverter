from flask import Flask, render_template, abort, jsonify, request
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        # form has been submitted, process data
        URL = {"URL: ": request.form['yt_URL']}
    else: 
        return render_template("mp4converter.html")
    

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    url = request.json['url']
    yt = YouTube(url)
    video_info = {
        'title': yt.title,
        'thumbnail_url': yt.thumbnail_url,
        'duration': yt.length,
        'streams': {}
    }

    for stream in yt.streams.filter(file_extension='mp4').order_by('resolution'):
        if stream.resolution not in video_info['streams']:
            video_info['streams'][stream.resolution] = stream.url
    return jsonify(video_info)