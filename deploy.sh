rm -rf build dist Main.spec

pyinstaller -w -F Main.py

cp -r config dist/config
