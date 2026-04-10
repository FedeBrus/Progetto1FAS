#!/usr/bin/env bash

REMOTE="https://github.com/cldf-datasets/wals.git"
FILES=("values.csv" "languages.csv" "countries.csv" "codes.csv" "parameters.csv")
DATASET_DIR="./dataset"
CLONED_DIR="./wals_temp"

declare -A HEADERS
HEADERS["values.csv"]="Language_ID,Parameter_ID,Code_ID"
HEADERS["parameters.csv"]="ID,Name"
HEADERS["languages.csv"]="ID,Name,Latitude,Longitude,Country_ID"
HEADERS["countries.csv"]="ID,Name"
HEADERS["codes.csv"]="ID,Parameter_ID,Name,Description"

fetch() {
  echo "Starting fetch..."

  [[ -d "$CLONED_DIR" ]] && rm -rf "$CLONED_DIR"
  [[ ! -d "$DATASET_DIR" ]] && mkdir -p "$DATASET_DIR"

  echo "Cloning dataset from $REMOTE..."
  git clone "$REMOTE" "$CLONED_DIR"

  echo "Moving dataset's files..."
  for target in "${FILES[@]}"; do
    if [[ -f "$CLONED_DIR/cldf/$target" ]]; then
      echo "Moving $target in $DATASET_DIR..."
      mv "$CLONED_DIR/cldf/$target" "$DATASET_DIR/"
    fi
  done

  echo "Removing temporary $CLONED_DIR folder..."
  rm -rf "$CLONED_DIR"
  echo "[FETCH success]"
}

prune() {
  echo "Starting prune..."

  if [[ ! -d "$DATASET_DIR" ]]; then
    echo "Error: Directory $DATASET_DIR not found. Execute 'fetch' first."
    exit 1
  fi

  for file in "{$FILES[@]}"; do
    if [[ -f "$DATASET_DIR/$file" ]]; then
      cols=${HEADERS[$file]}

      if [[ -n $cols ]]; then
        echo "Pruning $file (keeping: $cols)..."
        xsv select "$cols" "$DATASET_DIR/$file" | sponge "$DATASET_DIR/$file"
      else
        echo "Error: No headers were specified for this file"
        exit 1
      fi
    fi
  done

  echo "[PRUNE success]"
}

usage() {
  echo "Usage: $0 {fetch|prune}"
  exit 1
}

case "$1" in
fetch)
  fetch
  ;;
prune)
  prune
  ;;
*)
  usage
  ;;
esac
