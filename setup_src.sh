#!/bin/bash
# Run from the root of your guitar-lesson-classifier/ project
# Usage: bash setup_src.sh

mkdir -p src tests

touch src/__init__.py
touch src/config.py
touch src/preprocessor.py
touch src/evaluate.py
touch src/train.py

touch tests/__init__.py
touch tests/test_preprocessor.py
touch tests/test_evaluate.py

echo "Done! Folders and files created."
