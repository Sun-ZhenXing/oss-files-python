@echo off
if "%UPX_PATH%" == "" (
  echo Please set UPX_PATH to the path of upx.exe directory
  goto :EOF
)

python -m nuitka ^
  --standalone ^
  --mingw64 ^
  --follow-imports ^
  --include-package-data=aliyunsdkcore ^
  --plugin-enable=pyside6,upx ^
  --output-dir=dist ^
  --upx-binary=%UPX_PATH% ^
  --windows-icon-from-ico=resources\icon.ico ^
  --include-data-dir=resources=resources ^
  --python-flag=no_docstrings,no_asserts ^
  --assume-yes-for-downloads ^
  --windows-console-mode=disable ^
  --show-progress ^
  --remove-output ^
  --main=main.py

:EOF
