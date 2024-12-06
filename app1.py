from flask import Flask, request, send_file, render_template
from transformers import VitsModel, AutoTokenizer
import scipy.io.wavfile
import torch
import numpy as np
import io

# Inicializar modelo y tokenizador
model = VitsModel.from_pretrained("facebook/mms-tts-yor")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Obtener el texto del formulario
    text = request.form["text"]
    
    # Procesar el texto para TTS
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform

    # Normalizar y convertir el audio a formato WAV
    audio_data = output.squeeze().numpy()
    audio_data_normalized = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

    # Guardar el archivo en un buffer en memoria
    buffer = io.BytesIO()
    scipy.io.wavfile.write(buffer, rate=model.config.sampling_rate, data=audio_data_normalized)
    buffer.seek(0)

    return send_file(buffer, as_attachment=False, download_name="output_yoruba.wav", mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
