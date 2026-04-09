#!/usr/bin/env bash

REMOTE="https://github.com/cldf-datasets/wals.git"
FILES=("values.csv" "languages.csv" "countries.csv" "language_names.csv" "codes.csv" "parameters.csv")

DATASET_DIR="./dataset"
CLONED_DIR="./wlas"

if [[ -d "$CLONED_DIR" ]]; then
  rm -rf "$CLONED_DIR"
fi

if [[ ! -d "$DATASET_DIR" ]]; then
  mkdir "$DATASET_DIR"
fi

git clone $REMOTE $CLONED_DIR
cd "$CLONED_DIR/cldf" || exit

echo "Pruning unused files..."

for file in *; do
  for target in "${FILES[@]}"; do
    if [[ "$file" == "$target" ]]; then
      echo "Moving $file file into $DATASET_DIR"
      mv "$file" "../../$DATASET_DIR"
      break
    fi
  done
done

cd ../.. && rm -rf "$CLONED_DIR"
