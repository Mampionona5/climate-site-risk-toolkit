# Contribuer au projet

Merci de contribuer à Climate Site Risk Toolkit.

## Méthode de travail

1. Créer une branche ciblée depuis la branche principale.
2. Installer le projet avec `python -m pip install -e ".[dev]"`.
3. Ajouter ou mettre à jour les tests pour chaque changement de comportement.
4. Exécuter `ruff check .`, `mypy src` et `pytest`.
5. Garder les demandes de fusion limitées et expliquer leur résultat pour l'utilisateur.

## Standards du code

- Utiliser des annotations de type et des docstrings pour les fonctions publiques.
- Séparer les calculs métier des opérations de lecture et d'écriture.
- Privilégier des exemples et des tests déterministes.
- Ne jamais enregistrer de données réelles confidentielles, personnelles ou institutionnelles.
- Documenter toute nouvelle source et sa licence dans `docs/PROVENANCE.md`.

## Messages de commit

Utiliser un résumé à l'impératif, par exemple :

```text
Ajoute la validation des indicateurs mensuels de chaleur
```

