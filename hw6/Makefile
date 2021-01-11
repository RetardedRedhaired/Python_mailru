all: migrate

up:
	docker-compose up

migrate: celery
	docker-compose exec web /manage.py migrate

redis: up
	redis-server --port 7777

celery: redis
	celery -A hw6 -b redis beat
