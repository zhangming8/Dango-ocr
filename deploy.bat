
set save_name=DangoOCR_windows_v1
set main=main

scp configs2.py configs.py

del/s/q build\*.*
rd/s/q build
del/s/q dist\*.*
rd/s/q dist
del %main%.spec
del %save_name%.rar

pyinstaller -D -w -i config\logo.ico %main%.py
scp -r config dist\%main%

ren "dist\%main%\%main%.exe" DangoOCR.exe
ren "dist\%main%" "%save_name%"
scp *.TTC dist

cd dist
"C:\Program Files\WinRAR\Rar.exe" a "%save_name%.rar" "%save_name%" *.TTC
cd ..

move "dist\%save_name%.rar" .\

del/s/q build\*.*
rd/s/q build
del/s/q dist\*.*
rd/s/q dist
del %main%.spec

echo "done, save to: %save_name%.rar"
