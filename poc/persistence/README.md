# Persistence POCs

- PostgreSQL : modèle hybride relationnel + JSONB, contrainte unique d'idempotence.
- MongoDB : document workflow et validation à faire côté application.
- SQLite : démonstrateur exécutable de concurrence et d'idempotence ; SQLite ne valide pas
  le comportement de concurrence PostgreSQL, mais permet de vérifier l'invariant fonctionnel.
