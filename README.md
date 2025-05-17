# Components and connections
https://wokwi.com/projects/430691449936658433
![image](https://github.com/user-attachments/assets/e346eb71-61cd-4bca-bb4c-4cc91bfd2d34)


# grblHAL RP2040 Firmware Build Instructions

This repository contains configuration and build instructions for compiling **grblHAL** for the RP2040 (Raspberry Pi Pico) using ARM GCC, CMake, and Ninja, producing .uf2 firmware images.

## Prerequisites

### 1. ARM GCC Toolchain

- Download and install ARM GNU Toolchain (e.g., arm-none-eabi-gcc).

### 2. CMake

- Install via your package manager or from cmake.org.

### 3. Ninja

- Install via your package manager or from ninja-build.org.

### 4. Pico SDK

```bash
cd ~
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git checkout sdk-<version>  # e.g. sdk-1.5.0
```
---
## Environment Setup

Add the following to your shell profile (~/.bashrc, ~/.zshrc, etc.):

```bash
export PICO_SDK_PATH=~/pico-sdk
export PATH="$PATH:/path/to/arm-none-eabi/bin"
```
---

## Building grblHAL for RP2040

## Clone the Repository

```bash
git clone https://github.com/<your-org>/grblHAL-rp2040.git
cd grblHAL-rp2040
```

## Prepare Custom Files

Overwrite the files in DrawbotDaVinci/modifiedRP2040files with the versions from your RP2040 board.

Create a settings.json file inside .vscode/ in the grblHAL-rp2040 directory.

Open the project in Visual Studio Code.

Use the CMake Tools extension to configure and select a build folder.

Click Build to generate the .uf2 firmware image.

Note: The latest working firmware (grblHAL.uf2) is available on the main page of the DrawbotDaVinci repository.

## Generating G-code from Images

img2gcode python file using potrace, ffmpeg, imagemagick (and autotrace)
Install the required programs following https://github.com/schollz/img2gcode
Use the modified img2gcode file from this project's files
Example commands for img2gcode when the image is placed in the same folder:

python img2gcode.py --file imagefilename.png --animate --simplify 1 --threshold 42
python img2gcode.py --file imagefilename.png --animate --simplify 3 --threshold 8

or alternatively
Inkscape + Gcodetools

## Install Inkscape

Download: https://inkscape.org

Add Gcodetools Extension

### Download the extension
git clone https://github.com/kliment/gcodetools

### Copy the folder (and its .inx/.py files) into:
C:\Program Files\Inkscape\share\extensions

Tutorial

Watch: https://www.youtube.com/watch?v=6b_XMrfLMc0

Transferring G-code to the Machine

## Universal Gcode Sender

Download: https://winder.github.io/ugs_website/

Connect & Set up (first time onely)

Open UGS, connect the device using setup wizard.
On the calibration screen of setup wizard, set steps per millimeter to the following:

X: 41.667
Y: 43.448
Z: Any, not used

(Measured with a ruler, possibly off by half a millimeter)

Enabling microstepping:
Run the command (or add it to the beginnig of the code)
M64 P0 M64 P1 M64 P2 M64 P3
The modified img2gcode adds this line to the beginning automatically.


Load the generated .gcode file.

