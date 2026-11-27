# C1 — MongoDB

Le document `workflow.example.json` représente un workflow avec nœuds et arêtes imbriqués.
À mesurer sur MongoDB : lecture complète, mise à jour d'un paramètre, validation des références,
atomicité d'une mise à jour et intégrité des références user/subscription/execution.
MongoDB permet l'atomicité au niveau document ; les relations inter-documents et la déduplication
doivent être conçues explicitement (index unique sur `{workflow_id,event_id}`).
