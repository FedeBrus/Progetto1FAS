#!/usr/bin/env bash

source "./utils.sh"

echo "Starting prune..."

# $DATASET_DIR doesn't exist
if [[ ! -d "$DATASET_DIR" ]]; then
  echo "ERROR: Directory $DATASET_DIR not found. Execute 'fetch' first, aborting prune..."
  exit 1
fi

# $RAW_DIR doesn't exist
if [[ ! -d "$RAW_DIR" ]]; then
  echo "ERROR: Directory $RAW_DIR not found. Execute 'fetch' first, aborting prune..."
  exit 1
fi

for file in "${TARGET_FILES[@]}"; do
  if [[ -f "$RAW_DIR/$file" ]]; then
    cols=${HEADERS[$file]}

    if [[ -n $cols ]]; then
      echo "Pruning $file (keeping: $cols)..."

      if [[ -n "${RENAMES[$file]}" ]]; then
        xan select "$cols" "$RAW_DIR/$file" | xan rename "${RENAMES[$file]}" -s "Name" | sponge "$RAW_DIR/$file"
      else
        xan select "$cols" "$RAW_DIR/$file" | sponge "$RAW_DIR/$file"
      fi
    else
      echo "ERROR: No headers were specified for this file, aborting prune..."
      exit 1
    fi
  fi
done

echo "[PRUNE success]"