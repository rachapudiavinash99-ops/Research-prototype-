.PHONY: start build test

start:
	docker-compose up

build:
	docker-compose build

test:
	pytest backend/tests/
