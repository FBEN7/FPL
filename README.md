# fantasy-football-tool

Outil data pour la Fantasy Premier League. Phase 1 : usage personnel, pour
apprendre le jeu et Python. Public visé plus tard : anglophone.

## Lancer

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Tests : `.venv/bin/python -m pytest -q`

## Contenu

- `ffdata/api.py` : lecture de l'API publique du jeu, avec cache disque (`.cache/`).
- `ffdata/analysis.py` : tableaux joueurs, meilleur rapport points/prix,
  calendrier et difficulté des matchs, ton équipe.
- `app.py` : tableau de bord Streamlit (3 onglets).

## Plan (5 h/semaine)

**Phase 1, novembre 2026 → mars 2027 : apprendre**
- Semaine 1 : créer ton équipe (gratuit, on peut rejoindre en cours de saison)
  et lancer le tableau de bord.
- Chaque semaine : 1 h pour jouer avec l'outil, 1 h pour lire r/FantasyPL
  et noter les besoins non couverts, 3 h pour coder une amélioration.
- Fin mars 2027 : décision (rester perso, ou lancer publiquement).

**Phase 2, avril → août 2027 : lancer**
- Une seule fonctionnalité différenciante, choisie d'après les notes.
- Mise en ligne gratuite avant la première deadline de la saison 2027/28.
- Revenus par le contenu (newsletter, Patreon), pas par la revente des données.

## Règles

- Les CGU du jeu (art. 28 b et d, 29) interdisent l'extraction automatisée
  et l'usage commercial des données. L'écosystème d'outils est toléré, mais
  rien n'est garanti. Tout passe par le cache, sans requêtes inutiles.
- Pas de « Premier League », « FPL », logos ni écussons de clubs dans le nom
  ou le visuel du produit.
- Avant le premier euro gagné : statut d'indépendant complémentaire en Belgique.
