#!/bin/bash

echo "Running external verification..."

python analysis/external_minimal_verifier.py

if [ $? -eq 0 ]; then
  echo "Verification PASSED"
else
  echo "Verification FAILED"
fi
