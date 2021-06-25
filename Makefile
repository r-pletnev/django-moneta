run_build:
	python -m build --outdir build

clean_after_build:
	rm -rf django_payanyway.egg-info
	rm  -rf build/lib
	rm -rf build/bdist.linux-x86_64

app: run_build clean_after_build

uninstall:
	pip uninstall django-moneta -y

install:
	pip install build/django-moneta-0.1.tar.gz

reinstall: uninstall install

test:
	pytest moneta -vv