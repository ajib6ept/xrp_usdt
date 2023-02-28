install:
	poetry install

lint:
	@poetry run flake8 xrp-usdt tests

mypy:
	poetry run mypy --strict xrp-usdt

test:
	poetry run pytest -vvs
	
test-coverage:
	poetry run coverage run --source=xrp-usdt -m pytest tests
	poetry run coverage xml

xrp-usdt:
	poetry run python xrp-usdt/main.py	

.PHONY: test xrp-usdt