from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

CRITIC_PROMPT = """Tu es un expert en contrôle qualité de recherche.
On te donne une question de recherche et une synthèse.
Ton rôle est d'évaluer si la synthèse répond bien à la question.

Tu réponds UNIQUEMENT avec ce format JSON, rien d'autre :
{
    "score": [0 à 10],
    "pertinent": [true ou false],
    "raison": "[explication courte]"
}

Critères :
- Score 8-10 : synthèse pertinente et factuelle
- Score 5-7 : partiellement pertinente
- Score 0-4 : hors sujet ou trop vague
- pertinent = true si score >= 5"""


def run_critic(question: str, synthese: str) -> dict:
    """Évalue la qualité d'une synthèse par rapport à sa question."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": CRITIC_PROMPT},
            {
                "role": "user",
                "content": f"Question : {question}\n\nSynthèse : {synthese}"
            }
        ]
    )

    raw = response.choices[0].message.content

    # Parse le JSON
    import json
    try:
        evaluation = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback si le LLM n'a pas respecté le format
        evaluation = {
            "score": 5,
            "pertinent": True,
            "raison": "Format inattendu, synthèse conservée par défaut"
        }

    return evaluation


# Test
if __name__ == "__main__":
    # Simule une bonne synthèse
    bonne_synthese = {
        "question": "Quels pays africains adoptent les EVs ?",
        "synthese": "L'Afrique du Sud et le Maroc sont leaders. Des incitations fiscales sont en place."
    }

    # Simule une mauvaise synthèse
    mauvaise_synthese = {
        "question": "Quels pays africains adoptent les EVs ?",
        "synthese": "Les Émirats arabes unis et l'Arabie saoudite investissent massivement dans les EVs."
    }

    for s in [bonne_synthese, mauvaise_synthese]:
        eval = run_critic(s["question"], s["synthese"])
        print(f"Question : {s['question']}")
        print(f"Score    : {eval['score']}/10")
        print(f"Pertinent: {eval['pertinent']}")
        print(f"Raison   : {eval['raison']}")
        print()