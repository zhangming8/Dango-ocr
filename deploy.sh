rm -rf build dist Main.spec

# pyinstaller -D -w Main.py
pyinstaller -w -F Main.py

cp -r config dist/config
