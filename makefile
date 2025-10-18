.PHONY: tests run sort freeze


run:
	uvicorn main:app --reload

freeze:
	pip freeze > requirements.txt

sort:
	isort .

tests:
	ENV=test python -m pytest

coverage:
	ENV=test python -m pytest --cov=. --cov-report=html
