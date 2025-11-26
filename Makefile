install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

lint:
	uv run ruff check task_manager

start-server:
	cd code && . /project/.venv/bin/activate && python manage.py runserver 0.0.0.0:3000