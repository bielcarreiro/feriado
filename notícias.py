import os
import requests
from dotenv import load_dotenv

load_dotenv() # Carrega a API lá da buceta

# Função para obter notícias
def obter_noticias():
    chave_api = os.getenv("NEWS_API")
    url = (
        f'https://newsapi.org/v2/top-headlines?'
        f'country=br&apiKey={chave_api}'
    )

    try:
        resposta = requests.get(url)
        noticias = resposta.json()

        if noticias["status"] == "ok":
            # Retorna os 3 firts títulos 
            noticias_formatadas = [
                f"{i+1}. {artigo['title']}" for i, artigo in enumerate(noticias["articles"][:3])
            ]
            return "Aqui estão as últimas notícias:\n" + "\n".join(noticias_formatadas)
        else:
            return "Não consegui buscar as notícias no momento."
    except Exception as e:
        return f"Ocorreu um erro ao obter notícias: {str(e)}"