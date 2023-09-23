from dotenv import load_dotenv
from elevenlabs import generate, play, set_api_key
from googleapiclient.discovery import build
from googletrans import Translator
from langdetect import detect
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import requests
import json
import datetime
import random
import os
import tempfile
import pywhatkit
# Inicializar el reconocimiento de voz y el motor de síntesis de voz
recognizer = sr.Recognizer()

# Cargar variables de entorno
load_dotenv()
# API KEY de OpenWeatherMap
api_key = os.environ.get("API_KEY")
# API KEY de Google
api_key_google = os.environ.get("API_KEY_GOOGLE")
# ID del motor de búsqueda de Google
search_engine_id = os.environ.get("SEARCH_ENGINE_ID")
# API KEY de Eleven Labs
eleven_labs_api_key = os.environ.get("ELEVEN_LABS_API_KEY")
# Función para escuchar el comando de voz


def escuchar_comando():
    with sr.Microphone() as source:
        print("Escuchando comando...")
        recognizer.adjust_for_ambient_noise(source)
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
    set_api_key(eleven_labs_api_key)
    audio = generate(
        text=respuesta,
        voice="Bella",
        model='eleven_multilingual_v1'
    )

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        temp_file.write(audio)
        temp_filename = temp_file.name
    audio_segment = AudioSegment.from_file(temp_filename, format="mp3")
    play(audio_segment)

    os.remove(temp_filename)


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


saludos = [
    "¡Hola! ¿Cómo puedo ayudarte?",
    "¡Hola! ¿En qué puedo ayudarte hoy?",
    "¡Saludos! ¿En qué puedo asistirte?",
    "¡Buen día! ¿En qué puedo colaborar contigo?",
    "¡Hola! ¿En qué puedo servirte?",
    "¡Saludos! ¿Cómo puedo ser de utilidad?",
    "¡Hola! ¿Qué puedo hacer por ti en este momento?",
    "¡Buenas! ¿Cómo puedo ayudarte hoy?",
    "¡Hola! ¿En qué puedo brindarte apoyo?",
    "¡Saludos! ¿En qué puedo contribuir a tu día?"
]
respuestas_aqui = [
    "¡Aquí estoy!",
    "Aquí presente.",
    "Lista para ayudarte.",
    "A tu disposición.",
    "Lista y atento.",
    "Aquí para asistirte.",
    "Presente y disponible.",
    "Dispuesto a colaborar.",
    "Aquí, lista para servirte.",
    "Presente y lista."
]
respuestas_ciudad = [
    "Por favor, indícame la ciudad para obtener el clima.",
    "Necesito que me digas la ciudad para brindarte la información climática.",
    "¿Cuál es la ciudad de la que deseas conocer el clima?",
    "Por favor, especifica la ciudad para obtener el pronóstico del tiempo.",
    "Dime el nombre de la ciudad para la que quieres saber el clima.",
    "¿De qué ciudad te gustaría conocer el clima?",
    "Necesito que me proporciones el nombre de la ciudad para obtener el clima actual.",
    "Por favor, indica la ciudad de la que quieres obtener el clima actualizado.",
    "¿Cuál es la ciudad que deseas consultar para obtener el clima?",
    "Indícame la ciudad y te diré cómo está el clima allí."
]
# función para realizar la búsqueda en Google:


def buscar_en_google(query):
    service = build("customsearch", "v1", developerKey=api_key_google)
    result = service.cse().list(q=query, cx=search_engine_id).execute()
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
    escucha_activa = False
    while True:
        comando = escuchar_comando()
        if "alexa" in comando or "alexa" in comando:
            escucha_activa = True
            activa = random.choice(respuestas_aqui)
            hablar(activa)
        if escucha_activa:
            comando = escuchar_comando()
            if "hola" in comando:
                saludo = random.choice(saludos)
                hablar(saludo)
                print("comando ==> hola")
                escucha_activa = False
            elif "tiempo" in comando or "clima" in comando:
                # climas = random.choice(respuestas_ciudad)
                # hablar(climas)
                print("comando ==> tiempo")
                ciudad = comando.replace("clima", " ").replace("tiempo", " ").replace(
                    "en", " ").replace("de", " ").replace("la", " ").replace("el", " ").strip()
                resultado = obtener_clima(ciudad)
                if resultado:
                    clima, temperatura = resultado
                    hablar(
                        f"El clima en {ciudad} es {clima} y la temperatura es de {temperatura} grados Celsius.")
                    print("comando ==> clima respuesta")
                else:
                    hablar("No se pudo obtener el clima para esa ciudad.")
                    print("comando ==> clima no respuesta")
                escucha_activa = False
            elif "hora" in comando or "qué hora es" in comando:
                hora_actual = datetime.datetime.now().strftime("%H:%M")
                hablar(f"La hora exacta es {hora_actual}")
                print("comando ==> hora")
                escucha_activa = False
            elif "gracias" in comando:
                hablar(
                    "De nada, ¡estoy aquí para ayudar! Si tienes alguna otra pregunta, no dudes en hacerla.")
                print("comando ==> gracias")
                escucha_activa = False
            elif "ayudar" in comando or "ayuda" in comando:
                hablar(
                    "Te puedo ayudar con el clima de cualquier ciudad, la hora exacta en Colombia y también contarte unos chistes")
                print("comando ==> ayuda")
                escucha_activa = False
            elif "chiste" in comando or "cuenta un chiste" in comando:
                chiste = obtener_chiste()
                hablar(chiste)
                print("comando ==> chiste")
                escucha_activa = False
            elif "buscar" in comando:
                hablar("!!Qué quieres buscar.")
                print("comando ==> buscar")
                consulta = escuchar_comando()
                resultados = buscar_en_google(consulta)
                if resultados:
                    # Obtener el primer resultado de la lista
                    resultado = resultados[0]
                    titulo = resultado["title"]
                    descripcion = resultado["snippet"]
                    hablar(
                        f"Encontré este resultado: {titulo} {descripcion}")
                    print("comando ==> buscar respuesta")
                else:
                    hablar(
                        "Lo siento, no pude encontrar resultados para esa búsqueda.")
                    print("comando ==> buscar no respuesta")
                escucha_activa = False
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
                escucha_activa = False
            elif "traducir" in comando:
                hablar("Por favor, dime el texto que deseas traducir.")
                texto_a_traducir = escuchar_comando()
                hablar("¿A qué idioma deseas traducirlo?")
                idioma_destino = escuchar_comando()
                # Función auxiliar para traducir el nombre del idioma a código de idioma
                idioma_destino = traducir_nombre_idioma(idioma_destino)
                if idioma_destino:
                    idioma_texto = detect(texto_a_traducir)
                    if idioma_texto != "es":
                        # Traducir el texto al español si no está en español originalmente
                        texto_a_traducir = traducir(texto_a_traducir, "es")
                    texto_traducido = traducir(
                        texto_a_traducir, idioma_destino)
                    if texto_traducido:
                        hablar(
                            f"La traducción al {idioma_destino} es: {texto_traducido}")
                    else:
                        hablar("No se pudo realizar la traducción.")
                else:
                    hablar("El idioma especificado no es válido.")
                escucha_activa = False
            elif "reproducir" in comando or "reproduce" in comando:
                music = comando.replace(
                    "reproducir", " ").replace("reproduce", " ")
                hablar("Reproduciendo " + music)
                print("comando ==> reproducir")
                pywhatkit.playonyt(music)
            elif "adiós" in comando:
                hablar("¡Hasta luego!")
                print("comando ==> adiós")
                return False
            else:
                hablar("Lo siento, no puedo entender ese comando.")
                print("comando ==> no entendido")
                escucha_activa = False
            return True


while True:
    if not asistente_virtual():
        break
