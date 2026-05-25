from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

PLANNER_PROMPT = """Tu es un expert en recherche et analyse.
Ton rôle est de décomposer une question complexe en sous-questions de recherche.

Règles :
- Génère exactement 3 sous-questions
- Chaque sous-question doit être précise et searchable sur le web
- Réponds UNIQUEMENT avec une liste numérotée, rien d'autre

Format de réponse :
1. [sous-question]
2. [sous-question]
3. [sous-question]"""


def run_planner(question: str) -> list[str]:
    """Décompose une question en sous-questions de recherche."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": f"Question principale : {question}"}
        ]
    )

    raw = response.choices[0].message.content

    # Parse la liste numérotée en liste Python
    lines = raw.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Enlève le "1. " au début
            question_text = line.split(". ", 1)[1]
            questions.append(question_text)

    return questions


# Test
if __name__ == "__main__":
    question = "Analyse l'état du marché des EVs en Afrique en 2026"
    sous_questions = run_planner(question)

    print(f"Question principale : {question}\n")
    print("Sous-questions générées :")
    for i, q in enumerate(sous_questions, 1):
        print(f"{i}. {q}")