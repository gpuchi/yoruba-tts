from flask import Flask, request, send_from_directory, render_template
from transformers import VitsModel, AutoTokenizer
import scipy.io.wavfile
import torch
import numpy as np
import os

app = Flask(__name__)

# Configura el directorio de archivos estáticos para audio
OUTPUT_DIR = "static/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar modelo y tokenizador
model = VitsModel.from_pretrained("facebook/mms-tts-yor")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        text = request.form["text"]
        inputs = tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            output = model(**inputs).waveform

        # Normalizar y guardar archivo WAV
        audio_data = output.squeeze().numpy()
        audio_data_normalized = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
        audio_path = os.path.join(OUTPUT_DIR, "output_yoruba.wav")
        scipy.io.wavfile.write(audio_path, rate=model.config.sampling_rate, data=audio_data_normalized)

        # Guardar nombre del archivo para mostrarlo
        audio_file = "output_yoruba.wav"

    return render_template("index.html", audio_file=audio_file)

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
