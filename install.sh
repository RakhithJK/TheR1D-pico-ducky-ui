#!/bin/bash

# Check if wget is installed
command -v wget >/dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Wget is installed. You're good to go!"
else
    echo "Wget is not installed on your system."
    echo "Please install wget and try again."
fi

check_path_existence() {
  if [ -d "$1" ]; then
    echo "Found path: $1"
    return 0
  else
    return 1
  fi
}

if check_path_existence "/media/CIRCUITPY"; then
  target="/media/CIRCUITPY"
  echo "Found path: /media/CIRCUITPY"
elif check_path_existence "/Volumes/CIRCUITPY"; then
  target="/Volumes/CIRCUITPY"
  echo "Found path: /Volumes/CIRCUITPY"
else
  echo "Neither path /media/CIRCUITPY nor /Volumes/CIRCUITPY exists."
  read -p "Please enter the path to your CIRCUITPY volume: " target
fi

echo "Downloading Adafruit CircuitPython libraries..."
url="https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20230416/adafruit-circuitpython-bundle-8.x-mpy-20230416.zip"
wget "${url}"
echo "Unzipping Adafruit CircuitPython libraries..."
unzip "adafruit-circuitpython-bundle-8.x-mpy-20230416.zip"
echo "Installing libraries to CIRCUITPY..."
# Delete the test folder if it exists.
rm -rf "${target}/lib" || true
rm -rf "${target}/scripts" || true
mkdir -p "${target}/lib"
cp adafruit-circuitpython-bundle-8.x-mpy-20230416/lib/adafruit_ticks.mpy "${target}/lib/"
cp adafruit-circuitpython-bundle-8.x-mpy-20230416/lib/adafruit_debouncer.mpy "${target}/lib/"
cp -r adafruit-circuitpython-bundle-8.x-mpy-20230416/lib/adafruit_display_text "${target}/lib/"
cp -r adafruit-circuitpython-bundle-8.x-mpy-20230416/lib/adafruit_hid "${target}/lib/"
echo "Installing Rubber Ducky to CIRCUITPY..."
cp -f src/*.py "${target}/"
echo "Installing Rubber Ducky scripts CIRCUITPY..."
cp -r scripts "${target}/"
