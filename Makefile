enter:
	docker-compose -f local.yml run --rm django sh

test:
	docker-compose -f local.yml run --rm django pytest

newapp:
	docker-compose -f local.yml run --rm django python manage.py startapp  ${app}

makemigrations:
	docker-compose -f local.yml run --rm django python manage.py makemigration

migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate

createsuperuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

stop:
	docker-compose -f local.yml stop

kill:
	docker-compose -f local.yml down

start:
	docker-compose -f local.yml up

build:
	docker-compose -f local.yml build
