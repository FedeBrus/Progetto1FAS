#!/usr/bin/env bash

REMOTE="https://github.com/cldf-datasets/wals.git"
TARGET_FILES=("values.csv" "languages.csv" "countries.csv" "codes.csv" "parameters.csv")
DATASET_DIR="../dataset"
TMP_DIR="$DATASET_DIR/tmp"
PROCESSED_DIR="$DATASET_DIR/processed"
RAW_DIR="$DATASET_DIR/raw"

prompt_for_overwrite() {
  dir=$1

  if [[ -e "$dir" ]]; then

    if [[ "$y_flag" -eq 1 ]]; then
        rm -rf "$dir"
        return 0
    fi

    read -p "$dir already exists, do you want to overwrite it? [y/N] "

    if [[ "$REPLY" =~ ^([Yy][Ee][Ss]|[Yy])$ ]]; then
      rm -rf "$dir"
    else
      return 1
    fi
  fi

  return 0
} 

y_flag=0

print_usage() {
  printf "Usage: $1 [-y]"
}

while getopts 'y' flag; do
  case "${flag}" in
    y) y_flag=1 ;;
    *) print_usage $0
       exit 1 ;;
  esac
done

echo "Starting fetch..."

# Setup raw directory
if prompt_for_overwrite "$DATASET_DIR"; then
  echo "Creating dataset directory..."
  mkdir -p "$DATASET_DIR" "$RAW_DIR" "$PROCESSED_DIR"
else 
  echo "ERROR: Dataset directory preservation was requested, aborting fetch..."
  exit 1
fi

# Cloning
if prompt_for_overwrite "$TMP_DIR"; then
  echo "Cloning dataset from $REMOTE..."
  git clone "$REMOTE" "$TMP_DIR"
else
  echo "ERROR: Cannot clone into already existing folder, aborting fetch..."
  exit 1
fi

# Moving dataset's TARGET_FILES
echo "Moving dataset's target files..."
for target in "${TARGET_FILES[@]}"; do

  prompt_for_overwrite "$RAW_DIR/$target"

  tmp_path="$TMP_DIR/cldf/$target"

  if [[ -f "$tmp_path" ]]; then
    echo "Moving $target in $RAW_DIR/$target..."
    mv "$tmp_path" "$RAW_DIR/"
  else
    echo "ERROR: $tmp_path was not found, aborting fetch..."
    exit 1
  fi
done

echo "Removing temporary $TMP_DIR folder..."
rm -rf "$TMP_DIR"
echo "[FETCH success]"

