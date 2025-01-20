from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import os
import whisper

app = Flask(__name__)
model = whisper.load_model("medium")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def transcribe_video(video_file_path):
    audio_file_path = video_file_path.replace('.mp4', '.mp3')
    video = VideoFileClip(video_file_path)
    video.audio.write_audiofile(audio_file_path)
    segments = model.transcribe(audio_file_path)['segments']
    return segments

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        video_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_file_path)
        segments = transcribe_video(video_file_path)
        return jsonify({'segments': segments}), 200

if __name__ == '__main__':
    app.run(debug=True)
