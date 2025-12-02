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

check:
	uv run ruff check task_manager

test-coverage:
	uv run pytest --cov=task_manager --cov-report=xml