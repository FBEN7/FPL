# fantasy-football-tool

Outil data Fantasy Premier League, side project. Le propriétaire apprend
Python : code simple, lisible, sans abstraction inutile. Expliquer les
changements en français ; code, identifiants et interface en anglais.

## Règles

- Toute requête vers l'API passe par `ffdata/api.py` et son cache. Pas de
  boucle sur des centaines de joueurs ou d'équipes sans cache ni pause.
- Phase 1 = usage personnel : pas de fonction payante, pas de revente de données.
- Pas de « Premier League », « FPL », logos ou écussons dans le nom, le titre
  ou le visuel de l'application.
- Les tests (`pytest`) utilisent des données inventées, jamais le réseau.
