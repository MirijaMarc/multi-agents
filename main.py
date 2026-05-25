from agents.planner import run_planner
from agents.researcher import run_researcher
from agents.critic import run_critic
from agents.writer import run_writer
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def run_research_agent(question: str):
    """Orchestre tous les agents pour produire un rapport complet."""

    print(f"\n🔍 Question : {question}\n")
    print("=" * 50)

    # Étape 1 : Planner
    print("\n📋 Étape 1 : Planification...")
    sous_questions = run_planner(question)
    for i, q in enumerate(sous_questions, 1):
        print(f"  {i}. {q}")

    # Étape 2 : Researchers en parallèle
    print("\n🌐 Étape 2 : Recherches en parallèle...")
    start = time.time()

    syntheses = [None] * len(sous_questions)

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_researcher, q): i
            for i, q in enumerate(sous_questions)
        }
        for future in as_completed(futures):
            i = futures[future]
            syntheses[i] = future.result()
            print(f"  ✅ Recherche {i+1} terminée : {sous_questions[i][:50]}...")

    elapsed = time.time() - start
    print(f"\n  ⚡ Temps total de recherche : {elapsed:.1f}sec")

    # Étape 3 : Critic
    print("\n🔎 Étape 3 : Évaluation des synthèses...")
    syntheses_validees = []

    for s in syntheses:
        evaluation = run_critic(s["question"], s["synthese"])
        statut = "✅" if evaluation["pertinent"] else "❌"
        print(f"  {statut} Score {evaluation['score']}/10 — {evaluation['raison']}")

        if evaluation["pertinent"]:
            syntheses_validees.append(s)

    print(f"\n  📊 {len(syntheses_validees)}/{len(syntheses)} synthèses retenues")

    if not syntheses_validees:
        print("\n⚠️  Aucune synthèse valide. Arrêt du rapport.")
        return

    # Étape 4 : Writer
    print("\n✍️  Étape 4 : Rédaction du rapport...")
    rapport = run_writer(question, syntheses_validees)

    # Sauvegarde
    filename = "rapport.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(rapport)

    print(f"\n✅ Rapport sauvegardé dans {filename}")
    print("\n" + "=" * 50)
    print(rapport)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("   🤖 RESEARCH AGENT SYSTEM")
    print("=" * 50)

    question = input("\n❓ Quelle est votre question de recherche ?\n→ ").strip()

    if not question:
        print("⚠️  Aucune question saisie. Arrêt.")
    else:
        run_research_agent(question)