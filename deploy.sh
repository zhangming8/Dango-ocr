#!/usr/bin/env bash

save_name="DangoOCR_mac_v1"
main="main"

cp configs2.py configs.py

rm -rf build dist "${main}.spec" "${save_name}.rar"

pyinstaller -D -w -i config/logo.ico "${main}.py"
cp -r config "dist/${main}/"

mv "dist/${main}/${main}" "dist/${main}/DangoOCR"
mv "dist/${main}" "dist/${save_name}"
cp *.TTC dist/

cd dist
rar a "${save_name}.rar" "${save_name}" *.TTC

cd ..

mv "dist/${save_name}.rar" ./

rm -rf build dist "${main}.spec"

echo "done, save to: ${save_name}.rar"
