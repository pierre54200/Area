# A1/A2/A3/A4 — PostgreSQL

Avec un PostgreSQL local ou Docker :
1. `psql "$DATABASE_URL" -f schema.sql`
2. Insérer un workflow comportant 1 trigger, 4 reactions et 1 condition ; noter le nombre de lignes.
3. Vérifier JSONB : `EXPLAIN ANALYZE SELECT ... WHERE params @> ...`.
4. Lancer deux transactions concurrentes insérant le même `(workflow_id,event_id)` : une seule doit réussir.
5. Backup/restore : `pg_dump "$DATABASE_URL" -Fc -f area.dump`; créer une base vide puis
   `pg_restore -d "$RESTORE_DATABASE_URL" area.dump`; comparer les nombres de lignes.
Ne pas conclure sur les performances sans noter versions, dataset et configuration.
