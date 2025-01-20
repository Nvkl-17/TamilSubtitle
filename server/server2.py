from flask import Flask, request, jsonify
from translator import VideoToTextTranslator

app = Flask(__name__)
model_path = "medium"  # Path to your Whisper model
video_translator = VideoToTextTranslator(model_path)

@app.route("/translate_video", methods=["POST"])
def translate_video():
    # Check if the POST request contains a file
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    # Check if the file is of allowed type
    if file and file.filename.lower().endswith((".mp4", ".avi", ".mov")):
        # Save the file temporarily
        file_path = "temp_video_file.mp4"
        file.save(file_path)
        # Translate the video to text
        result_segments = video_translator.translate_video_to_text(file_path)
        os.remove(file_path)  # Remove the temporary video file
        return jsonify({"result": result_segments})
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
