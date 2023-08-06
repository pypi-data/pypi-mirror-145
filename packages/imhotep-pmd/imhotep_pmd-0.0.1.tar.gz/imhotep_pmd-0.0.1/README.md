# imhotep_pmd

An [Imhotep](https://github.com/justinabrahms/imhotep) plugin for [PMD](https://pmd.github.io/), the static analyzer.

PMD talk to it via the Static Analysis Results Interchange Format (sarif), which is simply a JSON with a specific schema.

## Installation

## Usage

To use the plugin, you'll have to pass a path to the linter in question to the imhotep runtime.

```shell
imhotep --linter imhotep_pmd.plugin:PmdLinter
```
