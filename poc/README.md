# AREA — Proofs of Concept

POCs réalisés localement à partir de `docs/tech/{front,back,db}.md`.
Aucun commit ni push n'a été effectué.

## Statut de cette campagne

| Domaine | POC | Artefact | Vérification locale |
|---|---|---|---|
| Front | A1 React DOM / B1 RN Web | écrans de connexion comparables | structure HTML inspectable ; audit axe/Lighthouse à lancer avec dépendances |
| Front | A2 Expo / B2 RN Web Android / C1 Ionic / D1 Flutter | squelettes et commandes de build | non exécuté : toolchains mobiles absentes |
| Front | B2 mini-builder | composant React Flow web-only | non exécuté : dépendances npm non installées |
| Front | X2/X3 | contrat OpenAPI + package partagé TS | contrat fourni ; compilation TS non exécutée |
| Back | A1 Django + DRF | endpoint API + OpenAPI | non exécuté : Django non installé |
| Back | A2 OIDC | configuration allauth | non exécuté : fournisseur OIDC requis |
| Back | A3 Celery | tâche et déduplication persistée | logique de déduplication testable via POC persistence |
| Back | A4 OpenAPI | test de conformité minimal | exécuté avec Python standard |
| Back | B1 NestJS / C1 Spring | mêmes routes et contrat | squelettes fournis ; toolchains non installées |
| DB | A1/A2/A3/A4 PostgreSQL | schéma SQL, JSONB, unicité, backup | SQL fourni ; Docker/PostgreSQL absents |
| DB | C1 MongoDB | document équivalent | exemple fourni ; MongoDB absent |
| DB | D1 SQLite | concurrence/déduplication | exécuté avec SQLite local |

Les résultats non exécutés ne sont pas présentés comme des mesures. Les POCs nécessitant Docker,
PostgreSQL, MongoDB, Android SDK, Flutter ou des dépendances npm restent à lancer dans un environnement
équipé. Les commandes et critères de mesure sont indiqués dans chaque sous-dossier.

## Reproduire les tests exécutables

Depuis la racine du dépôt :

```bash
python poc/persistence/sqlite/run_poc.py
python poc/backend/openapi_contract/test_contract.py
```

## Arborescence

- `frontend/` : mêmes cas d'usage et variantes d'interface.
- `backend/` : endpoints équivalents, auth, hooks et contrat OpenAPI.
- `persistence/` : modèle relationnel/JSONB, MongoDB et test SQLite.
- `shared/` : contrat OpenAPI et types partagés.
- `RESULTS.md` : synthèse, mesures disponibles et limites.
