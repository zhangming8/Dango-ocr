#!/usr/bin/env bash
rm -rf build dist Main.spec

## windows
# pyinstaller -D -w -i config\logo.ico main.py

## ubuntu
pyinstaller -w -F main.py

cp -r config dist/config
