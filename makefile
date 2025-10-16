.PHONY: tests run


tests:
	ENV=test python -m pytest

run:
	uvicorn main:app --reload
