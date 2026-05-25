from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

client = Groq()
tavily = TavilyClient()

RESEARCHER_PROMPT = """Tu es un analyste de recherche expert.
On te donne une question et des résultats de recherche web bruts.
Ton rôle est de synthétiser ces informations en un paragraphe clair et factuel.

Règles :
- Reste factuel, pas d'opinion
- Cite les faits importants
- 100 à 150 mots maximum
- Réponds directement, sans introduction"""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def search_web(query: str) -> list:
    """Recherche web avec retry automatique."""
    results = tavily.search(query=query, max_results=3)
    return results.get("results", [])


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def synthesize(question: str, raw_content: str) -> str:
    """Synthèse LLM avec retry automatique."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": RESEARCHER_PROMPT},
            {"role": "user", "content": f"Question : {question}\n\nRésultats :\n{raw_content}"}
        ]
    )
    return response.choices[0].message.content


def run_researcher(question: str) -> dict:
    """Cherche sur le web et synthétise les résultats."""

    # Étape 1 : recherche web
    try:
        results = search_web(question)
    except Exception as e:
        print(f"  ⚠️  Recherche échouée après 3 tentatives : {e}")
        return {
            "question": question,
            "synthese": "Recherche indisponible pour cette question.",
            "sources": [],
            "erreur": True
        }

    if not results:
        return {
            "question": question,
            "synthese": "Aucun résultat trouvé pour cette question.",
            "sources": [],
            "erreur": True
        }

    # Formate les résultats
    raw_content = ""
    sources = []
    for r in results:
        raw_content += f"Source : {r.get('url', 'inconnue')}\n"
        raw_content += f"Contenu : {r.get('content', '')}\n\n"
        if r.get('url'):
            sources.append(r['url'])

    # Étape 2 : synthèse
    try:
        synthese = synthesize(question, raw_content)
    except Exception as e:
        print(f"  ⚠️  Synthèse échouée après 3 tentatives : {e}")
        return {
            "question": question,
            "synthese": "Synthèse indisponible pour cette question.",
            "sources": sources,
            "erreur": True
        }

    return {
        "question": question,
        "synthese": synthese,
        "sources": sources,
        "erreur": False
    }