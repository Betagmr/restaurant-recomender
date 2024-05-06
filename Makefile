install:
	poetry install --sync --no-root

create-db:
	python3 -m src.create_db