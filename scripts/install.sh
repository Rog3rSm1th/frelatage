#!/bin/bash

# This script is used to test the program during development. 
# usage : ./scripts/install.sh

echo "[+] Deleting older sources..."
rm -rf "`pip3 show frelatage| grep "Location: *"|sed "s/Location: //g"`/frelatage"
echo "[+] Uninstalling previous versions of frelatage..."
yes | pip3 uninstall frelatage
echo "[+] Deleting older wheels..."
rm dist/*
echo "[+] Building..."
poetry build
echo "[+] Installing frelatage..."
find ./dist -name 'frelatage-*.*.*.whl' -exec pip3 install {} \;
echo "[+] Installation completed"