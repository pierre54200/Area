# B1 — NestJS

Routes à exposer : POST `/api/auth/register`, POST `/api/auth/login`, GET/POST `/api/workflows`,
PATCH `/api/workflows/:id/enabled`. Générer Swagger avec `@nestjs/swagger` et comparer le document
au contrat commun. Pour les hooks, BullMQ + Redis ; pour la persistance, Prisma/TypeORM.
