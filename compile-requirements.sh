#!/bin/bash
# Make sure that the `pip-tools` package is already
# installed in the running environment.

pip-compile --output-file=requirements/compiled-dev.txt --resolver=backtracking requirements/dev.txt
pip-compile --output-file=requirements/compiled-production.txt --resolver=backtracking requirements/production.txt
