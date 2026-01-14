MIGRATE_UP=alembic upgrade head
MIGRATE_DOWN=alembic downgrade base

.PHONY: migrate downgrade

migrate:
	$(MIGRATE_UP)

downgrade:
	$(MIGRATE_DOWN)
