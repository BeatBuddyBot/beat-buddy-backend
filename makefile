BLACK_EXCLUDE = "(.venv|alembic)/.*"

.PHONY: run
run:
	uvicorn main:app --reload

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: sort
sort:
	isort --profile black .

.PHONY: black
black:
	black --exclude  $(BLACK_EXCLUDE) .

.PHONY: format
format: sort black


.PHONY: tests
tests:
	ENV=test python -m pytest

.PHONY: coverage
coverage:
	ENV=test python -m pytest --cov=. --cov-report=html

.PHONY: ci-sort
ci-sort:
	isort --check-only --profile black .

.PHONY: ci-black
ci-black:
	black --check --exclude $(BLACK_EXCLUDE) .

.PHONY: ci-format
ci-format: ci-sort ci-black

.PHONY: ci-coverage
ci-coverage:
	ENV=test python -m pytest   --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=.  | tee pytest-coverage.txt
