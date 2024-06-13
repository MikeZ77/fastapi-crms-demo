run-dev:
	fastapi dev app/main.py

run:
	fastapi run app/main.py

up:
	docker-compose up

up-build:
	docker-compose up --build

down: 
	docker-compose down

down-volume:
	docker-compose down --volumes

up-test-stack:
	docker-compose -f docker-compose.yml -f docker-compose-test.yml up -d

down-test-stack:
	docker-compose -f docker-compose.yml -f docker-compose-test.yml down --volumes

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

tets-e2e:
	pytest -m e2e