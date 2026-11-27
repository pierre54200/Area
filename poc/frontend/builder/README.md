# B2 — Mini builder RN Web + React Flow

Le builder est explicitement web-only, conformément à l'option B documentée.
L'idée est de garder les écrans communs en RN et d'isoler le canvas dans un fichier `.web.tsx`.
Exécuter avec React Flow installé et vérifier qu'aucun import du builder n'est résolu côté Android.
