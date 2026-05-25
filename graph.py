from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from agents.planner import run_planner
from agents.researcher import run_researcher
from agents.critic import run_critic
from agents.writer import run_writer
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


# L'état qui circule entre tous les agents
class ResearchState(TypedDict):
    question: str
    sous_questions: list[str]
    syntheses: list[dict]
    syntheses_validees: list[dict]
    rapport: str


# ── Nodes ──────────────────────────────────────────

def node_planner(state: ResearchState) -> ResearchState:
    """Node 1 : décompose la question."""
    print("\n📋 Planner en cours...")
    sous_questions = run_planner(state["question"])
    for i, q in enumerate(sous_questions, 1):
        print(f"  {i}. {q}")
    return {"sous_questions": sous_questions}


def node_researcher(state: ResearchState) -> ResearchState:
    """Node 2 : recherches en parallèle."""
    print("\n🌐 Recherches en parallèle...")
    start = time.time()
    sous_questions = state["sous_questions"]
    syntheses = [None] * len(sous_questions)

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_researcher, q): i
            for i, q in enumerate(sous_questions)
        }
        for future in as_completed(futures):
            i = futures[future]
            syntheses[i] = future.result()
            print(f"  ✅ Recherche {i+1} terminée")

    elapsed = time.time() - start
    print(f"  ⚡ Temps : {elapsed:.1f}sec")
    return {"syntheses": syntheses}


def node_critic(state: ResearchState) -> ResearchState:
    """Node 3 : filtre les synthèses."""
    print("\n🔎 Évaluation des synthèses...")
    syntheses_validees = []

    for s in state["syntheses"]:
        evaluation = run_critic(s["question"], s["synthese"])
        statut = "✅" if evaluation["pertinent"] else "❌"
        print(f"  {statut} Score {evaluation['score']}/10 — {evaluation['raison']}")
        if evaluation["pertinent"]:
            syntheses_validees.append(s)

    print(f"\n  📊 {len(syntheses_validees)}/{len(state['syntheses'])} retenues")
    return {"syntheses_validees": syntheses_validees}


def node_writer(state: ResearchState) -> ResearchState:
    """Node 4 : rédige le rapport."""
    print("\n✍️  Rédaction du rapport...")
    syntheses = state["syntheses_validees"]

    if not syntheses:
        return {"rapport": "⚠️ Aucune synthèse valide pour générer un rapport."}

    rapport = run_writer(state["question"], syntheses)
    return {"rapport": rapport}


# ── Construction du graphe ─────────────────────────

def build_graph():
    graph = StateGraph(ResearchState)

    # Ajoute les nodes
    graph.add_node("planner", node_planner)
    graph.add_node("researcher", node_researcher)
    graph.add_node("critic", node_critic)
    graph.add_node("writer", node_writer)

    # Définit les transitions
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "critic")
    graph.add_edge("critic", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


# ── Point d'entrée ─────────────────────────────────

def run_research_agent(question: str):
    print(f"\n{'='*50}")
    print("   🤖 RESEARCH AGENT SYSTEM (LangGraph)")
    print(f"{'='*50}")
    print(f"\n🔍 Question : {question}")

    app = build_graph()

    result = app.invoke({"question": question})

    rapport = result["rapport"]

    # Sauvegarde
    with open("rapport.md", "w", encoding="utf-8") as f:
        f.write(rapport)

    print(f"\n✅ Rapport sauvegardé dans rapport.md")
    print(f"\n{'='*50}")
    print(rapport)


if __name__ == "__main__":
    question = input("\n❓ Quelle est votre question ?\n→ ").strip()
    if question:
        run_research_agent(question)
    else:
        print("⚠️  Aucune question saisie.")