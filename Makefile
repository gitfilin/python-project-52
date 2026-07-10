install:
	uv sync

build:
	./build.sh

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

test:
	uv run python manage.py test

test-coverage:
	uv run coverage run --source=users,statuses,labels,tasks,task_manager manage.py test
	uv run coverage xml

start:
	uv run gunicorn task_manager.wsgi

render-start:
	gunicorn task_manager.wsgi
