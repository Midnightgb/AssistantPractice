import requests
import json

# Clave de API
api_key = "906c0d456ef5bd01efa7f8073030b9aa"

# ID de voz a utilizar
voice_id = "MF3mGyEYCl7XYWbV9V6O"

# Texto a convertir en habla
texto = "auuuuuuuuuuu como los lobos, awww ayyyyy"

# Parámetros de la solicitud
params = {
    "optimize_streaming_latency": 0,
    "labels": "accent",
    "value": "spanish"
}

# Encabezados de la solicitud
headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json"
}

# Cuerpo de la solicitud
data = {
    "text": texto,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
    }
}

# Realizar la solicitud POST a la API de Eleven Labs
response = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
    headers=headers,
    params=params,
    data=json.dumps(data)
)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Obtener el flujo de audio de la respuesta
    audio_stream = response.content

    # Guardar el audio en un archivo local
    with open("audio.mp3", "wb") as f:
        f.write(audio_stream)

    # Reproduce el archivo de audio utilizando un reproductor de audio externo
    import subprocess
    subprocess.run(
        ["C:/Program Files/Windows Media Player/wmplayer.exe", "audio.mp3"])

else:
    print("Error al obtener la síntesis de voz. Código de respuesta:",
          response.status_code)
