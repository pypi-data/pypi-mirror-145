# imhotep_pmd

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

An [Imhotep](https://github.com/justinabrahms/imhotep) plugin for [PMD](https://pmd.github.io/), the static analyzer.

PMD talk to it via the Static Analysis Results Interchange Format (sarif), which is simply a JSON with a specific schema.

## Installation

This package is available on [PyPI](https://pypi.org/project/imhotep-pmd/).

```shell
pip install imhotep_pmd
```

You'll have to install Imhotep itself as well, as this package is simply a binding.

```shell
pip install imhotep
```

Again, since this package is merely a binding, you need to install PMD as well. Please refer to their website for how.

An additional step is to provide a `imhotep_pmd.toml` at the root directory of the repo you want to run PMD against. It should contain this line that specifies the command used to invoke PMD:

```toml
pmd_command = "~/bin/pmd-bin-6.44.0/bin/run.sh pmd"
```

## Usage

To use the plugin, you'll have to pass a path to the linter in question to the imhotep runtime.

```shell
imhotep --linter imhotep_pmd.plugin:PmdLinter
```

## Demo
Let's take #1 as an example.

```shell
$ imhotep \
   --repo_name="tslmy/imhotep_pmd" \
   --github-username="tslmy" \
   --github-password="$GITHUB_PASSWORD" \
   --pr-number=1 \
   --linter imhotep_pmd.plugin:PmdLinter
```

Screenshots:

| Before | After |
| ------- | --- |
| ![Screen Shot 2022-04-03 at 14 04 45](https://user-images.githubusercontent.com/594058/161449329-7c43d6d8-547e-43a6-ac21-57701cb3b8fd.png) | ![Screen Shot 2022-04-03 at 14 27 11](https://user-images.githubusercontent.com/594058/161449378-6c20f0df-9785-43a0-99da-67a07574bb8e.png) |
