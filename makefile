.PHONY: tests run sort


tests:
	ENV=test python -m pytest

run:
	uvicorn main:app --reload

sort:
	isort .
