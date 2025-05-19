venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python -m venv venv
	source venv/bin/activate; pip install -Ur requirements.dev.txt
	touch venv/touchfile

test: venv
	source venv/bin/activate; cd src; ./manage.py test

style-check: venv
	source venv/bin/activate;
	isort -c src
	black --check src
	flake8 src

reformat: venv
	source venv/bin/activate;
	isort src
	black src

runserver: venv
	source venv/bin/activate; cd src; ./manage.py runserver

clean:
	rm -fr venv
	find -iname "*pyc" -delete
