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