import speech_recognition as sr
import pyttsx3
import requests
import json
import datetime
import random
from googleapiclient.discovery import build
from googletrans import Translator
from langdetect import detect
from pydub import AudioSegment
from pydub.playback import play
import io
# Inicializar el reconocimiento de voz y el motor de síntesis de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Clave de la API de OpenWeatherMap (obtén tu propia clave registrándote en https://openweathermap.org/)
API_KEY = "9b05e32f8f5fe5d603313c0b177b3b48"
API_KEY = "AIzaSyAJWxwTj-WKRS0GeAhhusMUPkpDLcituYs"
SEARCH_ENGINE_ID = "f7efbd8e8193d4976"
API_URL = "https://api-inference.huggingface.co/models/TurkuNLP/gpt3-finnish-small"
headers = {"Authorization": "Bearer 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"}

# Clave de la API de Eleven Labs (reemplaza con tu clave)
ELEVEN_LABS_API_KEY = "906c0d456ef5bd01efa7f8073030b9aa"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

#voice_id:"21m00Tcm4TlvDq8ikWAM" "name":"Rachel"
#"voice_id":"AZnzlk1XvdvUeBnXmlld","name":"Domi"
#voice_id":"EXAVITQu4vr4xnSDxMaL","name":"Bella"
#voice_id":"ErXwobaYiN019PkySvjV","name":"Antoni"
#voice_id":"MF3mGyEYCl7XYWbV9V6O","name":"Elli"
#voice_id":"TxGEqnHWrfWFTfGW9XjX","name":"Josh"
#voice_id":"VR6AewLTigWG4xSOukaG","name":"Arnold"
#voice_id":"pNInz6obpgDQGcFmaJgB","name":"Adam"
#voice_id":"yoZ06aMxZJJ28mfd3POQ","name":"Sam"
#voice_id":"GtyoNiTvtmEbOyA9jAMo","name":"julian"
#voice_id":"NYx0L9rKE06lkZoUSMOB","name":"daniel"
# Función para escuchar el comando de voz

def escuchar_comando():
    with sr.Microphone() as source:
        print("Escuchar comando...")
        audio = recognizer.listen(source)

        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            texto = texto.lower()
            if "raíz" in texto:  # Verificar si se menciona "raíz" en el comando
                # Reemplazar "raíz" por la función sqrt()
                texto = texto.replace("raíz", "sqrt")
            # Reemplazar "por" por el operador de multiplicación "*"
            # texto = texto.replace("por", "*")
            # texto = texto.replace("dividido", "/")
            # Reemplazar "a la" por el operador de potencia "**"
            # texto = texto.replace("ala", "**")
            # texto = texto.replace("raíz de", "sqrt")
            print(f"Has dicho: {texto}")
            return texto
        except sr.UnknownValueError:
            print("No se pudo reconocer el comando de voz.")
        except sr.RequestError:
            print("Error al conectar con el servicio de reconocimiento de voz.")

    return ""

# Función para hablar la respuesta
def hablar(respuesta):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }
    data = {
        "text": respuesta,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "accent": "Spanish"
        }
    }
    CHUNK_SIZE = 1024

    response = requests.post(url, json=data, headers=headers, stream=True)
    audio_chunks = []

    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            audio_chunks.append(chunk)

    audio = b''.join(audio_chunks)

    audio_segment = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
    play(audio_segment)


# Función para traducir

translator = Translator()
def traducir(texto, destino):
    try:
        translator = Translator()
        traduccion = translator.translate(texto, dest=destino)
        texto_traducido = traduccion.text
        return texto_traducido
    except Exception as e:
        print(f"Error al traducir: {e}")
        return None
    
# Función auxiliar para traducir el nombre del idioma a código de idioma
def traducir_nombre_idioma(nombre_idioma):
    if nombre_idioma.lower() == "español":
        return "es"
    elif nombre_idioma.lower() == "inglés":
        return "en"
    elif nombre_idioma.lower() == "francés":
        return "fr"
    # Agrega más idiomas según tus necesidades
    else:
        return None

# Función para obtener el clima de una ciudad específica

def obtener_clima(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid=9b05e32f8f5fe5d603313c0b177b3b48&lang=es&units=metric"
    respuesta = requests.get(url)
    datos = json.loads(respuesta.text)

    print(datos)  # Imprimir la respuesta completa para verificar su estructura

    if datos["cod"] == 404:
        return None
    else:
        clima = datos["weather"][0]["description"]
        temperatura = datos["main"]["temp"]
        return clima, temperatura

#Funcion ChatBot

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Función para obtener un chiste aleatorio


def obtener_chiste():
    lista_chistes = [
        "¿Qué le dice un semáforo a otro? No me mires, me estoy cambiando.",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
        "¿Qué le dice un jardinero a otro? Nos vemos cuando podamos.",
        "¿Cómo se llama el campeón de buceo japonés? Tokofondo. Y su hermano? Kasitoko.",
    ]
    return random.choice(lista_chistes)

# función para realizar la búsqueda en Google:


def buscar_en_google(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
    items = result.get("items", [])
    return items

# Función para realizar cálculos matemáticos


def calcular(expresion):
    try:
        resultado = eval(expresion)  # Evaluar la expresión matemática
        return resultado
    except Exception:
        return None

# Lógica principal del asistente


def asistente_virtual():
    comando = escuchar_comando()

    if "hola" in comando:
        hablar("¡Hola! ¿Cómo puedo ayudarte?")
        print("comando ==> hola")
    elif "tiempo" in comando or "clima" in comando:
        hablar("Por favor, dime la ciudad para la que quieres conocer el clima.")
        print("comando ==> tiempo")
        # Para que el asistente reconozca la ciudad y no la vea como  un comando no reconocido si no como un valor.
        ciudad = escuchar_comando()
        resultado = obtener_clima(ciudad)
        if resultado:
            clima, temperatura = resultado
            hablar(
                f"El clima en {ciudad} es {clima} y la temperatura es de {temperatura} grados Celsius.")
            print("comando ==> clima respuesta")
        else:
            hablar("No se pudo obtener el clima para esa ciudad.")
            print("comando ==> clima no respuesta")
    elif "hora" in comando or "qué hora es" in comando:
        hora_actual = datetime.datetime.now().strftime("%H:%M")
        hablar(f"La hora exacta es {hora_actual}")
        print("comando ==> hora")
    elif "gracias" in comando:
        hablar(
            "De nada, ¡estoy aquí para ayudar! Si tienes alguna otra pregunta, no dudes en hacerla.")
        print("comando ==> gracias")
    elif "ayudar" in comando or "ayuda" in comando:
        hablar("Te puedo ayudar con el clima de cualquier ciudad, la hora exacta en colombia y tambien contarte unos chistes")
        print("comando ==> ayuda")
    elif "chiste" in comando or "cuenta un chiste" in comando:
        chiste = obtener_chiste()
        hablar(chiste)
        print("comando ==> chiste")
    elif "buscar" in comando:
        hablar("Por favor, dime qué quieres buscar.")
        print("comando ==> buscar")
        consulta = escuchar_comando()
        resultados = buscar_en_google(consulta)
        if resultados:
            # Obtener el primer resultado de la lista
            resultado = resultados[0]
            titulo = resultado["title"]
            descripcion = resultado["snippet"]
            hablar(
                f"Encontré este resultado: {titulo}. Aquí está la descripción: {descripcion}")
            print("comando ==> buscar respuesta")
        else:
            hablar("Lo siento, no pude encontrar resultados para esa búsqueda.")
            print("comando ==> buscar no respuesta")
    elif "calcular" in comando or "cálculo" in comando:
        hablar("Por favor, dime la expresión matemática que deseas calcular.")
        print("comando ==> calcular")
        expresion = escuchar_comando()
        resultado = calcular(expresion)
        if resultado is not None:
            hablar(f"El resultado de {expresion} es {resultado}")
            print("comando ==> calcular respuesta")
        else:
            hablar("Lo siento, no pude realizar el cálculo.")
            print("comando ==> calcular no respuesta")
    elif "traducir" in comando:
            hablar("Por favor, dime el texto que deseas traducir.")
            texto_a_traducir = escuchar_comando()
            hablar("¿A qué idioma deseas traducirlo? Di el nombre del idioma en español.")
            idioma_destino = escuchar_comando()
            idioma_destino = traducir_nombre_idioma(idioma_destino)  # Función auxiliar para traducir el nombre del idioma a código de idioma
            if idioma_destino:
                idioma_texto = detect(texto_a_traducir)
                if idioma_texto != "es":
                    texto_a_traducir = traducir(texto_a_traducir, "es")  # Traducir el texto al español si no está en español originalmente
                texto_traducido = traducir(texto_a_traducir, idioma_destino)
                if texto_traducido:
                    hablar(f"La traducción al {idioma_destino} es: {texto_traducido}")
                else:
                    hablar("No se pudo realizar la traducción.")
            else:
                hablar("El idioma especificado no es válido.")

    elif "adiós" in comando:
        hablar("¡Hasta luego!")
        print("comando ==> adiós")
        return False
    else:
        hablar("Lo siento, no puedo entender ese comando.")
        print("comando ==> no entendido")

    return True


while True:
    if not asistente_virtual():
        break
