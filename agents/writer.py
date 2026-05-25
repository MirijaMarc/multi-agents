from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

WRITER_PROMPT = """Tu es un expert en rédaction de rapports analytiques.
On te donne plusieurs synthèses de recherche sur un sujet.
Ton rôle est de rédiger un rapport final structuré en markdown.

Structure obligatoire :
# [Titre du rapport]

## Introduction
[2-3 phrases de contexte]

## [Section par grande thématique]
[Contenu basé sur les synthèses]

## Conclusion
[Points clés et perspectives]

Règles :
- Utilise uniquement les informations fournies
- Sois factuel et analytique
- 400 mots maximum"""


def run_writer(question_principale: str, syntheses: list[dict]) -> str:
    """Rédige le rapport final à partir des synthèses."""

    # Formate les synthèses pour le LLM
    contenu = ""
    for i, s in enumerate(syntheses, 1):
        contenu += f"Recherche {i} : {s['question']}\n"
        contenu += f"Synthèse : {s['synthese']}\n\n"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": WRITER_PROMPT},
            {
                "role": "user",
                "content": f"Sujet : {question_principale}\n\nSynthèses :\n{contenu}"
            }
        ]
    )

    return response.choices[0].message.content


# Test
if __name__ == "__main__":
    # On simule des synthèses pour tester le Writer seul
    syntheses_test = [
        {
            "question": "Ventes de EVs en Afrique",
            "synthese": "Le marché est en croissance avec l'Afrique du Sud et le Maroc en tête."
        },
        {
            "question": "Politiques gouvernementales sur les EVs",
            "synthese": "Plusieurs gouvernements africains introduisent des incitations fiscales."
        },
        {
            "question": "Infrastructure de recharge en Afrique",
            "synthese": "L'infrastructure reste limitée mais des investissements sont en cours."
        }
    ]

    rapport = run_writer(
        question_principale="Analyse du marché des EVs en Afrique en 2026",
        syntheses=syntheses_test
    )

    print(rapport)  