import streamlit as st
from graph import build_graph

# ── Config page ────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Research Agent System")
st.caption("Powered by LangGraph + Groq + Tavily")

# ── Input ──────────────────────────────────────────
question = st.text_input(
    "❓ Votre question de recherche",
    placeholder="Ex: Analyse le marché des EVs en Afrique en 2026"
)

run = st.button("🚀 Lancer la recherche", disabled=not question)

# ── Execution ──────────────────────────────────────
if run and question:

    # Zones d'affichage
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("⚙️ Progression")
        status = st.empty()
        log = st.container()

    with col2:
        st.subheader("📄 Rapport final")
        rapport_zone = st.empty()

    # Callbacks de progression
    with log:
        planner_expander = st.expander("📋 Planner", expanded=True)
        researcher_expander = st.expander("🌐 Researchers", expanded=True)
        critic_expander = st.expander("🔎 Critic", expanded=True)
        writer_expander = st.expander("✍️ Writer", expanded=True)

    try:
        status.info("🔄 Démarrage du système...")

        app = build_graph()

        # Collecte les étapes via stream
        rapport_final = ""
        sous_questions = []

        for step in app.stream({"question": question}):
            node_name = list(step.keys())[0]
            node_output = step[node_name]

            if node_name == "planner":
                sous_questions = node_output.get("sous_questions", [])
                with planner_expander:
                    for i, q in enumerate(sous_questions, 1):
                        st.write(f"{i}. {q}")
                status.info("🌐 Recherches en cours...")

            elif node_name == "researcher":
                syntheses = node_output.get("syntheses", [])
                with researcher_expander:
                    for i, s in enumerate(syntheses, 1):
                        st.write(f"✅ Recherche {i} terminée")
                        if not s.get("erreur"):
                            st.caption(s["synthese"][:150] + "...")
                status.info("🔎 Évaluation en cours...")

            elif node_name == "critic":
                validees = node_output.get("syntheses_validees", [])
                total = len(sous_questions)
                with critic_expander:
                    st.write(f"📊 {len(validees)}/{total} synthèses retenues")
                status.info("✍️ Rédaction du rapport...")

            elif node_name == "writer":
                rapport_final = node_output.get("rapport", "")
                with writer_expander:
                    st.write("✅ Rapport rédigé")

        # Affiche le rapport
        rapport_zone.markdown(rapport_final)
        status.success("✅ Recherche terminée !")

        # Bouton de téléchargement
        st.download_button(
            label="⬇️ Télécharger le rapport",
            data=rapport_final,
            file_name="rapport.md",
            mime="text/markdown"
        )

    except Exception as e:
        status.error(f"❌ Erreur : {e}")
        st.exception(e)