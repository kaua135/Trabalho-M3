from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_KEY")
BASE_URL = "http://www.omdbapi.com/"

app = FastAPI(
    title="API de Consulta de Filmes",
    description="Consulta título, ano e sinopse usando a OMDB API",
    version="1.0"
)

@app.get("/filme")
def consultar_filme(titulo: str):
    if not titulo:
        raise HTTPException(status_code=400, detail="Título não informado.")

    params = {
        "t": titulo,
        "apikey": API_KEY
    }

    resposta = requests.get(BASE_URL, params=params)

    if resposta.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na consulta à OMDB.")

    dados = resposta.json()

    if dados.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Filme não encontrado.")

    resultado = {
        "titulo": dados.get("Title"),
        "ano": dados.get("Year"),
        "sinopse": dados.get("Plot")
    }

    return resultado
