enter:
	docker-compose -f local.yml run --rm django sh

crawl:
	docker-compose -f local.yml run --rm crawler bash
jup:
	docker-compose -f local.yml run --rm jupyter sh

logs:
	docker-compose -f local.yml logs -f

test:
	docker-compose -f local.yml run --rm django pytest 
cov:
	docker-compose -f local.yml run --rm django coverage run -m pytest	

newapp:
	docker-compose -f local.yml run --rm django python manage.py startapp  ${app}

makemigrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate

createsuperuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

shell:
	docker-compose -f local.yml run --rm django python manage.py shell_plus --ipython
stop:
	docker-compose -f local.yml stop

kill:
	docker-compose -f local.yml down

start:
	docker-compose -f local.yml up

build:
	docker-compose -f local.yml build

enterp:	
	docker-compose -f production.yml run --rm django sh
