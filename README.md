Atlas Milieuthema's
====================


Requirements
------------

* Docker-Compose (required)


Developing
----------

Use `docker-compose` to start a local database.

	(sudo) docker-compose start

or

	docker-compose up

The API should now be available on http://localhost:8000/

To run an import, execute:

	./atlas_milieuthemas/manage.py run_import


To see the various options for partial imports, execute:

	./atlas_milieuthemas/manage.py run_import --help