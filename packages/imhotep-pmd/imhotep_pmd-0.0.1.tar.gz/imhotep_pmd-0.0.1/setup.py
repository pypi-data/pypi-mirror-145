from setuptools import find_packages, setup

setup(
    name="imhotep_pmd",
    version="0.0.1",
    packages=find_packages(),
    url="https://github.com/tslmy/imhotep_pmd",
    license="MIT",
    author="Mingyang Li",
    author_email="imhotep_pmd@myli.page",
    description="An Imhotep plugin for PMD, the static analyzer.",
    install_requires=["jsonschema", "requests"],
    entry_points={
        "imhotep_linters": [".py = imhotep_pmd.plugin:PmdLinter"],
    },
)
