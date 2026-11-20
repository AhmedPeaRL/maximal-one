#!/bin/bash

python -m pip install --require-hashes -r requirements-lock.txt

python3 sos_degree_scan.py
