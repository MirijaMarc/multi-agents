from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

def call_llm(system_prompt: str, user_message: str) -> str:
    """Fonction de base pour appeler le LLM."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return response.choices[0].message.content


# Test avec deux "personnalités" différentes
question = "C'est quoi l'intelligence artificielle ?"

# Personnalité 1 : expert technique
reponse_expert = call_llm(
    system_prompt="Tu es un expert en IA qui répond de façon technique et précise.",
    user_message=question
)

# Personnalité 2 : pédagogue pour enfants
reponse_simple = call_llm(
    system_prompt="Tu expliques les concepts comme si tu parlais à un enfant de 10 ans.",
    user_message=question
)

print("=== EXPERT ===")
print(reponse_expert)
print("\n=== SIMPLE ===")
print(reponse_simple)