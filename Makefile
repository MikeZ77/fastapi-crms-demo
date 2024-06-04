run-dev:
	fastapi dev app/main.py

run:
	fastapi run app/main.py

up:
	docker-compose up

down: 
	docker-compose down

down-volume:
	docker-compose down --volumes