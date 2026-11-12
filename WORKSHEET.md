# WORKSHEET — Pipeline InDrive

## Q1
- Batch : drivers, vehicles et zones. Ce sont des listes qui changent peu, chargées une fois par jour.
- Streaming : rides. Ce sont des courses qui arrivent chaque minute.
- Pourquoi différent : les listes changent rarement, donc une fois par jour suffit. Les courses arrivent tout le temps, donc on les charge souvent.
- Le fait : rides.
- Les dimensions : drivers, vehicles et zones.

## Q2
C'est de l'ELT. On charge les données brutes dans `raw`, puis on les nettoie avec du SQL dans Postgres (`staging`, puis `mart`). On transforme après le chargement.

## Q3
Une ligne = une course (un `ride_id`), avec le nom du chauffeur, sa note et sa zone de départ.

## Q4
```
 raw_rides | staging_rides | lignes_retirees
-----------+---------------+-----------------
      2740 |          2524 |             216
```

Les 216 lignes retirées :
- 132 courses avec un chauffeur qui n'existe pas (999)
- 88 courses avec un tarif à 0 ou moins
- 4 courses avec les deux problèmes
- 132 + 88 − 4 = 216

Pourquoi filtrer dans staging : un JOIN supprime les lignes sans le dire. Dans staging, la règle est écrite et on voit ce qui est retiré. Les marts partent ensuite de données propres.

## Q5
Il n'y a pas de doublon parce que chaque fichier supprime la table puis la recrée à partir de `raw`. Le résultat est le même à chaque fois.

Avec INSERT INTO, les lignes seraient ajoutées à chaque exécution. Après 3 exécutions, chaque course serait 3 fois dans la table.

## Q6
- `fare_amount` est additif : on peut l'additionner, le total a toujours un sens.
- `rating` est non-additif : c'est une note, pas une quantité.

SUM(rating) est faux parce que la note du chauffeur est répétée sur chacune de ses courses. Plus il a de courses, plus la somme grandit, mais sa note ne change pas. Il faut utiliser AVG(rating).