#!/usr/bin/env bash
rm -rf build dist Main.spec

## windows
# pyinstaller -D -w -i config\logo.ico Main.py

## ubuntu
pyinstaller -w -F Main.py

cp -r config dist/config
