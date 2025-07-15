.PHONY: up down check format migration migrations migrate superuser tests build

create_migration:
	PYTHONPATH=src alembic revision --autogenerate -m $(m)

upgrade:
	PYTHONPATH=src alembic upgrade head

downgrade:
	PYTHONPATH=src alembic downgrade -1

stamp:
	PYTHONPATH=src alembic stamp head

rename_image:
	PYTHONPATH=src python ./src/commands/rename_image.py $(dir_name)

tts:
	PYTHONPATH=src python ./src/commands/text_to_audio.py $(file_name)

get_path:
	PYTHONPATH=src python ./src/commands/get_file_path.py $(file_name)