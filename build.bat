@echo off
chcp 65001 >nul
echo Building Image Converter GUI...
pyinstaller --noconfirm --clean images_converter_gui.spec
echo.
echo ✅ Done! Check the dist\ImageConverterGUI directory.
pause
