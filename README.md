# 🤖 Research Agent System

> Système multi-agent autonome qui génère des rapports de recherche complets à partir d'une simple question — propulsé par LangGraph, Groq et Tavily.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)

---

## 🎯 Ce que ça fait

Tu poses une question. Le système produit un rapport structuré en markdown en moins de 30 secondes.

```
"Analyse le marché des EVs en Afrique en 2026"
                    ↓
        rapport.md complet et sourcé
```

---

## 🏗️ Architecture

```
User Input
    │
    ▼
┌─────────┐
│ Planner │  Décompose la question en 3 sous-questions
└────┬────┘
     │
     ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│Researcher 1│  │Researcher 2│  │Researcher 3│  ← parallèle
└────┬───────┘  └─────┬──────┘  └──────┬─────┘
     └────────────────┼─────────────────┘
                      │
                      ▼
               ┌────────────┐
               │   Critic   │  Filtre les synthèses hors-sujet
               └─────┬──────┘
                     │
                     ▼
               ┌────────────┐
               │   Writer   │  Rédige le rapport final
               └─────┬──────┘
                     │
                     ▼
                rapport.md
```

### Les agents

| Agent | Rôle |
|---|---|
| **Planner** | Décompose la question en sous-questions searchables |
| **Researcher** | Recherche web (Tavily) + synthèse LLM par sous-question |
| **Critic** | Évalue la pertinence de chaque synthèse (score /10) |
| **Writer** | Agrège les synthèses validées en rapport markdown structuré |

---

## ⚡ Points techniques

- **Parallélisation** — les 3 Researchers tournent simultanément via `ThreadPoolExecutor` (gain 3x sur le temps de recherche)
- **Orchestration LangGraph** — graphe d'états explicite, chaque agent est un node isolé
- **Retry automatique** — `tenacity` relance les appels API jusqu'à 3 fois en cas d'échec
- **Filtering intelligent** — le Critic écarte les synthèses hors-sujet avant la rédaction
- **Interface web** — Streamlit avec progression en temps réel et téléchargement du rapport

---

## 🛠️ Stack

```
LangGraph     — orchestration du graphe d'agents
Groq API      — inférence LLM (LLaMA 3.3 70B)
Tavily API    — recherche web optimisée pour les agents IA
Streamlit     — interface utilisateur
Tenacity      — retry et résilience des appels API
Python 3.12   — langage principal
```

---

## 🚀 Installation

```bash
# Clone le repo
git clone https://github.com/TON_USERNAME/research-agent
cd research-agent

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Dépendances
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env
# → Remplis GROQ_API_KEY et TAVILY_API_KEY dans .env
```

---

## 🔑 Configuration

Crée un fichier `.env` à la racine :

```env
GROQ_API_KEY=ta_clé_groq
TAVILY_API_KEY=ta_clé_tavily
```

- Groq API key : [console.groq.com](https://console.groq.com) (gratuit)
- Tavily API key : [tavily.com](https://tavily.com) (gratuit en dev)

---

## 💻 Usage

### Interface web (recommandé)

```bash
streamlit run app.py
# → ouvre http://localhost:8501
```

### Terminal

```bash
python graph.py
# → tape ta question et le rapport est généré dans rapport.md
```

---

## 📁 Structure

```
research-agent/
├── agents/
│   ├── __init__.py
│   ├── planner.py       # Décompose la question
│   ├── researcher.py    # Recherche web + synthèse
│   ├── critic.py        # Évalue la pertinence
│   └── writer.py        # Rédige le rapport final
├── app.py               # Interface Streamlit
├── graph.py             # Graphe LangGraph + orchestration
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📄 Licence

MIT