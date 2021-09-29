from setuptools import (
    setup,
)

extras_require = {
    "test": [
        "pytest-django",
        "pytest",
        "pytest-dotenv",
    ],
    "dev": [
        "ipython",
    ],
}

extras_require["dev"] = extras_require["dev"] + extras_require["test"]


setup(
    name="django-payanyway",
    url="https://github.com/r-pletnev/django-moneta",
    license="GPL",
    description="Moneta(PayAnyWay)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Roman Pletnev",
    author_email="ge52@mail.ru",
    install_requires=["django>=2", "pydantic", "zeep", "pydash"],
    python_require=">=3.7",
    extras_require=extras_require,
    packages=["moneta"],
    include_package_data=True,
    zip_safe=False,
)
