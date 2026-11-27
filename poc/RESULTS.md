# Résultats de la campagne POC

## Résumé

Cette archive fournit une base d'expérimentation et des implémentations de référence. Elle ne contient
pas de mesures de performance mobile ou de build Docker : l'environnement d'exécution ne dispose ni
de Docker, ni d'Android SDK/Flutter, ni des serveurs PostgreSQL/MongoDB. Les POCs concernés sont
préparés mais doivent être exécutés sur une machine équipée.

## Front-end

| POC | Comparaison | Résultat observé |
|---|---|---|
| A1 vs B1 | HTML sémantique React DOM vs primitives RN Web | Deux implémentations sont fournies ; aucun score axe/Lighthouse n'est revendiqué |
| A2/C1/D1 | APK natif / WebView / Flutter | Squelettes et instructions ; build non exécuté |
| B2 | builder RN Web + React Flow web-only | Exemple isolé fourni |

Mesures à relever : Lighthouse Accessibility (même version, viewport, build production), nombre
d'issues axe par sévérité, navigation clavier, labels/annonces, taille APK, temps de build.

## Back-end

| POC | Résultat |
|---|---|
| A1/B1/C1 | Contrats de routes équivalents documentés dans le fichier OpenAPI ; exemples Django, NestJS et Spring |
| A2 | Configuration django-allauth illustrative ; nécessite un client OIDC réel |
| A3 | Déduplication conçue autour d'une contrainte unique persistée ; redémarrage Celery non mesuré |
| A4 | Test de cohérence minimal OpenAPI exécuté avec succès |

Le test de contrat vérifie les routes et méthodes déclarées contre un manifeste d'implémentation
minimal. Ce n'est pas un substitut à Schemathesis contre un serveur réel.

## Persistance

| POC | Résultat |
|---|---|
| PostgreSQL A1/A2 | Schéma relationnel et exemple JSONB fournis ; non exécuté |
| PostgreSQL A3 / SQLite D1 | Déduplication par clé unique : test concurrent SQLite exécuté |
| PostgreSQL A4 | commandes `pg_dump` / `pg_restore` documentées ; non exécutées |
| MongoDB C1 | document équivalent fourni ; comparaison de latence non exécutée |

## Conclusion provisoire

Les choix documentaires restent cohérents avec les artefacts : React DOM pour l'accessibilité web,
Django/DRF pour l'intégration fonctionnelle, PostgreSQL pour les transactions et la contrainte unique.
Cette campagne ne fournit pas encore de preuve suffisante pour modifier les scores initiaux. Les mesures
manquantes doivent être collectées avant de transformer ces tendances en décision expérimentale.
