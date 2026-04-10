#!/usr/bin/env bash

# Pruning unused columns

DATASET_DIR="./dataset"

xsv select '!ID,Value,Comment,Source,Example_ID' "$DATASET_DIR/values.csv" | sponge "$DATASET_DIR/values.csv"
