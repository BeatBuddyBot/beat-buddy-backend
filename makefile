.PHONY: tests run


tests:
	python -m pytest

run:
	uvicorn main:app --reload
