#!/usr/bin/env bash

REMOTE="https://github.com/cldf-datasets/wals.git"
FILES=("values.csv" "languages.csv" "countries.csv" "codes.csv" "parameters.csv")
DATASET_DIR="./dataset"
CLONED_DIR="./wals_temp"

RAW_DIR="$DATASET_DIR/raw"

declare -A HEADERS
HEADERS["values.csv"]="Language_ID,Parameter_ID,Code_ID"
HEADERS["parameters.csv"]="ID,Name"
HEADERS["languages.csv"]="ID,Name,Latitude,Longitude,Country_ID"
HEADERS["countries.csv"]="ID,Name"
HEADERS["codes.csv"]="ID,Name,Description"

declare -A RENAMES
RENAMES["languages.csv"]="Language_Name"
RENAMES["parameters.csv"]="Parameter_Name"
RENAMES["codes.csv"]="Code_Name"
RENAMES["countries.csv"]="Country_Name"

FINAL_PATH="$DATASET_DIR/features.csv"

fetch() {
  echo "Starting fetch..."

  [[ -d "$CLONED_DIR" ]] && rm -rf "$CLONED_DIR"
  [[ ! -d "$DATASET_DIR" ]] && mkdir -p "$DATASET_DIR" "$RAW_DIR"

  echo "Cloning dataset from $REMOTE..."
  git clone "$REMOTE" "$CLONED_DIR"

  echo "Moving dataset's files..."
  for target in "${FILES[@]}"; do
    if [[ -f "$CLONED_DIR/cldf/$target" ]]; then
      echo "Moving $target in $RAW_DIR..."
      mv "$CLONED_DIR/cldf/$target" "$RAW_DIR/"
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
  elif [[ ! -d "$RAW_DIR" ]]; then
    echo "Error: Directory $RAW_DIR not found. Execute 'fetch' first."
    exit 1
  fi

  for file in "${FILES[@]}"; do
    if [[ -f "$RAW_DIR/$file" ]]; then
      cols=${HEADERS[$file]}

      if [[ -n $cols ]]; then
        echo "Pruning $file (keeping: $cols)..."

        xan select "$cols" "$RAW_DIR/$file" | {
          if [[ -n "${RENAMES[$file]}" ]]; then
            xan rename "${RENAMES[$file]}" -s "Name"
          else
            cat
          fi
        } | sponge "$RAW_DIR/$file"
      else
        echo "Error: No headers were specified for this file"
        exit 1
      fi
    fi
  done

  echo "[PRUNE success]"
}

join() {
  local file=$1
  local on_left=$2
  local on_right=$3

  echo "Joining $FINAL_PATH with $file on ($on_left = $on_right)..."

  xan join "$on_left" "$FINAL_PATH" "$on_right" "$file" |
    xan select "!$on_right" |
    sponge "$FINAL_PATH"
}

join_all() {
  echo "Starting join..."

  if [[ -e "$FINAL_PATH" ]]; then
    echo "Error: $FINAL_PATH already exists"
    exit 1
  fi

  echo "Copying values.csv into $FINAL_PATH..."
  cp "$RAW_DIR/values.csv" "$FINAL_PATH"

  join "$RAW_DIR/languages.csv" "Language_ID" "ID"
  join "$RAW_DIR/parameters.csv" "Parameter_ID" "ID"
  join "$RAW_DIR/codes.csv" "Code_ID" "ID"

  echo "[JOIN success]"
}

usage() {
  echo "Usage: $0 {fetch|prune|join}"
  exit 1
}

case "$1" in
fetch)
  fetch
  ;;
prune)
  prune
  ;;
join)
  join_all
  ;;
*)
  usage
  ;;
esac
