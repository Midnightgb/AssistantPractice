import requests

url = "https://api.elevenlabs.io/v1/voices"

headers = {
    "Accept": "application/json",
    "xi-api-key": "906c0d456ef5bd01efa7f8073030b9aa"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("resultado.txt", "w") as file:
        file.write(response.text)
        print("El archivo se ha exportado correctamente.")
else:
    print("Error al realizar la solicitud HTTP.")


urls = "https://api.elevenlabs.io/v1/voices/settings/default"

headerss = {
    "Accept": "application/json"
}

responses = requests.get(urls, headers=headerss)

if responses.status_code == 200:
    with open("settings.txt", "w") as file:
        file.write(responses.text)
        print("El archivo se ha exportado correctamente.")
else:
    print("Error al realizar la solicitud HTTP.")


url = "https://api.elevenlabs.io/v1/voices/GtyoNiTvtmEbOyA9jAMo/settings"

headers = {
    "Accept": "application/json",
    "xi-api-key": "906c0d456ef5bd01efa7f8073030b9aa"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("settingsVoice.txt", "w") as file:
        file.write(response.text)
        print("El archivo se ha exportado correctamente.")
else:
    print("Error al realizar la solicitud HTTP.")


url = "https://api.elevenlabs.io/v1/models"

headers = {
    "Accept": "application/json",
    "xi-api-key": "906c0d456ef5bd01efa7f8073030b9aa"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open("models.txt", "w") as file:
        file.write(response.text)
        print("El archivo se ha exportado correctamente.")
else:
    print("Error al realizar la solicitud HTTP.")
