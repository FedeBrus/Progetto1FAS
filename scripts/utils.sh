#!/usr/bin/env bash

REMOTE="https://github.com/cldf-datasets/wals.git"
TARGET_FILES=("values.csv" "languages.csv" "countries.csv" "codes.csv" "parameters.csv")
SCRIPT_DIR=$(dirname "$0")
DATASET_DIR="$SCRIPT_DIR/../dataset"
TMP_DIR="$DATASET_DIR/tmp"
PROCESSED_DIR="$DATASET_DIR/processed"
RAW_DIR="$DATASET_DIR/raw"

# Array associativo per le colonne da mantenere per ciascun file
declare -A HEADERS
HEADERS["values.csv"]="Language_ID,Parameter_ID,Code_ID"
HEADERS["parameters.csv"]="ID,Name"
HEADERS["languages.csv"]="ID,Name,Latitude,Longitude,Country_ID,Macroarea,Family,Subfamily,Genus"
HEADERS["countries.csv"]="ID,Name"
HEADERS["codes.csv"]="ID,Name"

# Array associativo per il rename delle colonne duplicate
declare -A RENAMES
RENAMES["languages.csv"]="Language_Name"
RENAMES["parameters.csv"]="Parameter_Name"
RENAMES["codes.csv"]="Code_Name"
RENAMES["countries.csv"]="Country_Name"

FINAL_PATH="$PROCESSED_DIR/features.csv"

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
