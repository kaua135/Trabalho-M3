from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

API_KEY = "37c31d83"

# Função para traduzir o texto para português usando MyMemory(usando a Ajuda do chat)
def traduzir(texto):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": texto,
        "langpair": "en|pt"
    }
    r = requests.get(url, params=params).json()
    return r.get("responseData", {}).get("translatedText", texto)


#  PÁGINA INICIAL DO MENU
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Busca de Filmes</title>
    </head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Buscar Filme</h1>
        <form action="/filme" method="get">
            <input type="text" name="titulo" placeholder="Digite o nome do filme" style="padding: 5px; width: 300px;">
            <button type="submit" style="padding: 5px 10px;">Buscar</button>
        </form>
    </body>
    </html>
    """


# ------------------- BUSCA DO FILME -------------------
@app.get("/filme", response_class=HTMLResponse)
def filme(titulo: str):
    url = f"http://www.omdbapi.com/?t={titulo}&apikey={API_KEY}"
    r = requests.get(url).json()

    if r.get("Response") == "False":
        return """
        <h1>Filme não encontrado </h1>
        <a href='/'>Voltar</a>
        """

    titulo = r.get("Title")
    ano = r.get("Year")
    sinopse_original = r.get("Plot")

    # TRADUZ A SINOPSE AUTOMATICAMENTE
    sinopse_traduzida = traduzir(sinopse_original)

    return f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Resultado da Busca</h1>

        <p><strong>Título:</strong> {titulo}</p>
        <p><strong>Ano:</strong> {ano}</p>
        <p><strong>Sinopse:</strong> {sinopse_traduzida}</p>

        <hr>

        <h3>Sinopse original (Inglês)</h3>
        <p>{sinopse_original}</p>

        <br><br>
        <a href="/">Buscar outro filme</a>
    </body>
    </html>
    """
