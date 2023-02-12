install:
	poetry install

lint:
	@poetry run flake8 xrp-usdt tests

test:
	poetry run pytest -vvs
	
test-coverage:
	poetry run coverage run --source=xrp-usdt -m pytest tests
	poetry run coverage xml

.PHONY: test, page_loader
