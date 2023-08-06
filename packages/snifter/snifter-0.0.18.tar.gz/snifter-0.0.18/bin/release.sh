#!/usr/bin/env bash
[[ "$TRACE" ]] && set -x
set -eu -o pipefail

tox -e clean && tox -e build && tox -e publish -- --repository pypi --verbose
