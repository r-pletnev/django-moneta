run_build:
	python -m build --outdir build

clean_after_build:
	rm -rf django_moneta.egg-info

app: run_build clean_after_build