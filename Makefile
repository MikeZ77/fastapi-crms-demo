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