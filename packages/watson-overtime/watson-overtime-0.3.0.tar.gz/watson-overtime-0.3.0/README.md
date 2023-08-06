[![Tests](https://github.com/flyingdutchman23/watson-overtime/workflows/Tests/badge.svg)](https://github.com/flyingdutchman23/watson-overtime/actions?workflow=Tests)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/flyingdutchman23/watson-overtime/main.svg)](https://results.pre-commit.ci/latest/github/flyingdutchman23/watson-overtime/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/watson-overtime)](https://img.shields.io/pypi/pyversions/watson-overtime)


# watson-overtime


## Description

This is a simple tool to calculate if a set working time is fulfilled for a
certain period of time. Therefore, it uses the time tracking software
[td-watson][https://pypi.org/project/td-watson/] as input.


## Usage

Generate a `watson report` in JSON format. This command e.g. generates a watson
report for the current for the project `PROJECT`. Pipe the output to
`watson-overtime`:
```bash
watson report -w -p PROJECT --json | watson-overtime
```
