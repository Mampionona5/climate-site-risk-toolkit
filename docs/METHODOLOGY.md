# Méthodologie

## Association spatiale

Chaque site est associé aux coordonnées de latitude et de longitude les plus proches dans
la grille. Les coordonnées réellement sélectionnées sont conservées dans la sortie détaillée
afin que cette approximation reste visible et contrôlable.

## Indicateurs mensuels

Pour chaque site et chaque mois :

- `mean_tmax_c` : moyenne arithmétique de la température maximale quotidienne ;
- `heat_days` : nombre de jours où `tmax_c` atteint ou dépasse le seuil de chaleur ;
- `total_precip_mm` : cumul des précipitations quotidiennes ;
- `heavy_rain_days` : nombre de jours atteignant ou dépassant le seuil de fortes pluies ;
- `dry_days` : nombre de jours avec moins de 1 mm de précipitations ;
- `stress_days` : nombre de jours franchissant le seuil de chaleur ou de fortes pluies.

Les seuils par défaut sont fixés à 35 °C et 20 mm par jour. Ils constituent des valeurs
d'exemple et doivent être adaptés au type de site, au territoire et à la décision visée.

## Contrôles de qualité

Avant tout calcul, le pipeline vérifie les dimensions, les variables, l'unicité des
coordonnées, la validité des dates, les valeurs manquantes, les identifiants de sites et les
plages autorisées pour les coordonnées géographiques.

## Limites connues

- La sélection de la cellule la plus proche ne réalise pas d'interpolation spatiale.
- L'outil ne quantifie pas les incertitudes des modèles climatiques.
- Les indicateurs ne représentent ni des dommages physiques ni un risque sanitaire.
- Le jeu d'exemple ne doit pas être interprété comme des observations ou des projections.

