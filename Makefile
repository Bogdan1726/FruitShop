MANAGE = python manage.py
PROJECT = config

# region local
run:
	$(MANAGE) runserver

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

test:
	$(MANAGE) test

shell:
	$(MANAGE) shell
# //

# management commands

generate_fruits:
	$(MANAGE) generate_fruits

generate_users:
	$(MANAGE) generate_test_users

create_bank:
	$(MANAGE) create_bank


# //



# Celery
start_worker:
	celery -A $(PROJECT) worker --loglevel=info

start_beat:
	celery -A $(PROJECT) beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

start_flower:
	celery -A $(PROJECT) flower --port=5555
# //