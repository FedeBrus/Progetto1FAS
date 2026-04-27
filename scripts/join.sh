#!/bin/bash

source "$(dirname "$0")/utils.sh"

join() {
  local file=$1
  local on_left=$2
  local on_right=$3

  echo "Joining $FINAL_PATH with $file on ($on_left = $on_right)..."

  xan join "$on_left" "$FINAL_PATH" "$on_right" "$file" | xan select "!$on_right" | sponge "$FINAL_PATH"
}

echo "Starting join..."

if ! prompt_for_overwrite "$FINAL_PATH"; then
  echo "ERROR: Final path preservation was requested, aborting join..."
  exit 1
fi

echo "Copying values.csv into $FINAL_PATH..."
cp "$RAW_DIR/values.csv" "$FINAL_PATH"

join "$RAW_DIR/languages.csv" "Language_ID" "ID"
join "$RAW_DIR/parameters.csv" "Parameter_ID" "ID"
join "$RAW_DIR/codes.csv" "Code_ID" "ID"

xan flatmap 'split(Country_ID, " ")' "Country_ID" -r "Country_ID" "$FINAL_PATH" | sponge "$FINAL_PATH"

join "$RAW_DIR/countries.csv" "Country_ID" "ID"

echo "[JOIN success]"

