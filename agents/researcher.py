from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

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


def run_researcher(question: str) -> dict:
    """Cherche sur le web et synthétise les résultats."""

    # Étape 1 : recherche web avec Tavily
    search_results = tavily.search(
        query=question,
        max_results=3
    )

    # Formate les résultats bruts pour le LLM
    raw_content = ""
    sources = []
    for result in search_results["results"]:
        raw_content += f"Source : {result['url']}\n"
        raw_content += f"Contenu : {result['content']}\n\n"
        sources.append(result["url"])

    # Étape 2 : synthèse par le LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": RESEARCHER_PROMPT},
            {"role": "user", "content": f"Question : {question}\n\nRésultats :\n{raw_content}"}
        ]
    )

    synthese = response.choices[0].message.content

    return {
        "question": question,
        "synthese": synthese,
        "sources": sources
    }


# Test
if __name__ == "__main__":
    question = "Quel est le nombre de véhicules électriques vendus en Afrique en 2026 ?"
    resultat = run_researcher(question)

    print(f"Question : {resultat['question']}\n")
    print(f"Synthèse :\n{resultat['synthese']}\n")
    print("Sources :")
    for s in resultat["sources"]:
        print(f"  - {s}")