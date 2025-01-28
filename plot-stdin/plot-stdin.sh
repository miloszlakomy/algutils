#!/usr/bin/env bash

# Reads a stream of floating-point values from stdin and plots them using braille ascii-art.
#
# Example:
#   seq 100 | ./plot-stdin.sh

# directory containing current script
readonly SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
# expected path to the virtualenv, in case we're not in one already
readonly VIRTUALENV_PATH='/tmp/plot-stdin-venv'

if [[ ! "$VIRTUAL_ENV" ]]; then
  echo "Not in virtualenv; using $VIRTUALENV_PATH"
  if [[ ! -d "$VIRTUALENV_PATH" ]]; then
    echo "virtualenv $VIRTUALENV_PATH doesn't exist, initializing"
    virtualenv "$VIRTUALENV_PATH"
  fi
  . "$VIRTUALENV_PATH/bin/activate"
fi

pip install -r "$SCRIPT_DIR/requirements.txt"

if [[ "$PROFILE" ]]; then
  python -m cProfile -o "$PROFILE" "$SCRIPT_DIR/plot-stdin.py"
else
  python "$SCRIPT_DIR/plot-stdin.py"
fi
