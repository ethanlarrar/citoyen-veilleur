help:
	@echo "To deploy, type:"
	@echo "ssh push myserver master"

install: bin/python

bin/python:
	virtualenv -p python3 .
	bin/pip install -r requirements.txt

serve: bin/python
	bin/python ./manage.py runserver 8000

deploy: bin/python
	DJANGO_SETTINGS_MODULE=mysite.settings_prod bin/python ./manage.py collectstatic --clear --noinput
	touch mysite/wsgi.py  # trigger reload

clean:
	rm -rf bin/ include/ lib/

