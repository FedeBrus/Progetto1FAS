#!/usr/bin/env bash

remote="https://github.com/cldf-datasets/wals.git"
target_files=("values.csv" "languages.csv" "countries.csv" "codes.csv" "parameters.csv")
dataset_dir="./dataset"
cloned_dir="./wals_temp"

raw_dir="$dataset_dir/raw"

# Array associativo per le colonne da mantenere per ciascun file
declare -A HEADERS
HEADERS["values.csv"]="Language_ID,Parameter_ID,Code_ID"
HEADERS["parameters.csv"]="ID,Name"
HEADERS["languages.csv"]="ID,Name,Latitude,Longitude,Country_ID,Macroarea,Family,Subfamily,Genus"
HEADERS["countries.csv"]="ID,Name"
HEADERS["codes.csv"]="ID,Name,Description,Number"

# Array associativo per il rename delle colonne duplicate
declare -A RENAMES
RENAMES["languages.csv"]="Language_Name"
RENAMES["parameters.csv"]="Parameter_Name"
RENAMES["codes.csv"]="Code_Name"
RENAMES["countries.csv"]="Country_Name"

FINAL_PATH="$DATASET_DIR/features.csv"

fetch() {
  echo "Starting fetch..."

  # Directories already exist
  if [[ -d "$CLONED_DIR" ]]; then 
    read -p "$CLONED_DIR already exists, do you want to overwrite it? [y/N]"

    if [[ "$REPLY" =~ ^([Yy][Ee][Ss]|[Yy])$ ]]; then
        rm -rf "$CLONED_DIR"
    else 
        echo "Fetch process was cancelled";
        exit 1
    fi
  fi
  
  if [[ -d "$DATASET_DIR" ]]; then
    # TODO: make this branch a function
    read -p "$DATASET_DIR already exists, do you want to overwrite it? [y/N]"

    if [[ "$REPLY" =~ ^([Yy][Ee][Ss]|[Yy])$ ]]; then
        rm -rf "$DATASET_DIR"
    else 
        echo "Fetch process was cancelled";
        exit 1
    fi
  else
    mkdir -p "$DATASET_DIR" "$RAW_DIR"
  fi

  # Cloning
  echo "Cloning dataset from $REMOTE..."
  git clone "$REMOTE" "$CLONED_DIR"

  # Moving dataset's TARGET_FILES
  echo "Moving dataset's TARGET_FILES..."
  for target in "${TARGET_FILES[@]}"; do
    if [[ -f "$CLONED_DIR/cldf/$target" ]]; then
      echo "Moving $target in $RAW_DIR..."
      mv "$CLONED_DIR/cldf/$target" "$RAW_DIR/"
    fi
  done

  echo "Removing temporary $CLONED_DIR folder..."
  rm -rf "$CLONED_DIR"
  echo "[FETCH success]"
}