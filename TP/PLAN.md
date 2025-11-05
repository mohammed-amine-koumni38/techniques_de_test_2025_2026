# TODO
# PLAN.md — Plan de tests du microservice Triangulator

 🎯 Objectif du projet
Le **Triangulator** est un microservice Flask chargé de calculer la **triangulation** d’un ensemble de points 2D (PointSet).  
Il reçoit un `PointSetID` du client, récupère les points correspondants auprès du service **PointSetManager**, calcule la triangulation, et renvoie le résultat sous forme binaire (Triangles).

L’objectif des tests est de garantir :
- le bon fonctionnement du service à toutes les étapes,
- la robustesse face aux erreurs possibles,
- la conformité aux formats binaires,
- et de mesurer les performances du calcul.

---

 🧱 1. Structure du projet de test

Les tests seront organisés dans le dossier `tests/` :
tests/
├── test_triangulation.py # Tests unitaires de l'algorithme
├── test_binary.py # Tests de conversion binaire
├── test_api.py # Tests de l'API Flask
└── test_performance.py # Tests de performance
2. Tests unitaires — Algorithme de triangulation
Fichier : `test_triangulation.py`

 Objectif :
Vérifier que la fonction `triangulate(points)` :
- renvoie des triangles corrects et cohérents,
- gère correctement les cas limites.

### Cas de test prévus :
 T1 | Triangulation simple
 T2 | Carré 
 T3 | Polygone convexe
 T4 | Points colinéaires 
 T5 | Points dupliqués
 T6 | Moins de 3 points 
 ## 💾 3. Tests unitaires — Conversion binaire

Fichier : `test_binary.py`

### Objectif :
Valider les fonctions `encode_pointset()`, `decode_pointset()`, `encode_triangles()`, `decode_triangles()`.

 Cas de test prévus :
 T1| Encodage/décodage simple 
 T2 | Format invalide
 T3 | Triangles encodés/décodés
 T4 | Zéro point

 4. Tests d’intégration — API Flask

 ichier : `test_api.py`

### Objectif :
Vérifier que l’API du Triangulator respecte sa spécification (`triangulator.yml`).

### Endpoints principaux :
- `POST /triangulate/<pointset_id>`

### Cas de test prévus :
T1 | Requête valide
T2 | PointSet inexistant
T3 | Erreur du PointSetManager
T4 | Données malformées
T5 | Test de bout en bout


LES étapes à suivre:
Étape 1 : écrire les tests unitaires (même s’ils échouent)

Étape 2 : implémenter la logique minimale pour les faire passer

Étape 3 : ajouter les tests d’intégration Flask

Étape 4 : ajouter les tests de performance

Étape 5 : vérifier la qualité (ruff, coverage, pdoc3)


°°Gestion des erreurs prévues

PointSet non trouvé → 404

Service PointSetManager inaccessible → 502

Format binaire invalide → 400

Erreur interne → 500

Ces cas seront simulés dans les test d'API

°°Critères de validation

Tous les tests passent (pytest ✅)

Couverture ≥ 90%

Lint sans erreur (ruff check ✅)

Documentation générée (pdoc3 ✅)

Structure et architecture conformes au cahier des charges










 
