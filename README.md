grblHAL RP2040 Firmware Build Instructions

This repository contains configuration and build instructions for compiling grblHAL for the RP2040 (Raspberry Pi Pico) using ARM GCC, CMake, and Ninja, producing .uf2 firmware images.

Prerequisites

ARM GCC Toolchain

Download and install ARM GNU Toolchain (e.g., arm-none-eabi-gcc).

CMake

Install via your package manager or from cmake.org.

Ninja

Install via your package manager or from ninja-build.org.

Pico SDK

cd ~
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git checkout sdk-<version>  # e.g. sdk-1.5.0

Environment Setup

Add the following to your shell profile (~/.bashrc, ~/.zshrc, etc.):

export PICO_SDK_PATH=~/pico-sdk
export PATH="$PATH:/path/to/arm-none-eabi/bin"

Building grblHAL for RP2040

Clone the Repository

git clone https://github.com/<your-org>/grblHAL-rp2040.git
cd grblHAL-rp2040

Prepare Custom Files

Overwrite the files in DrawbotDaVinci/modifiedRP2040files with the versions from your RP2040 board.

Create a settings.json file inside .vscode/ in the grblHAL-rp2040 directory.

Configure & Build

Open the project in Visual Studio Code.

Use the CMake Tools extension to configure and select a build folder.

Click Build to generate the .uf2 firmware image.

Note: The latest working firmware (grblHAL.uf2) is available on the main page of the DrawbotDaVinci repository.

Generating G-code from Images

Inkscape + Gcodetools

Install Inkscape

Download: https://inkscape.org

Add Gcodetools Extension

# Download the extension
git clone https://github.com/kliment/gcodetools

# Copy the folder (and its .inx/.py files) into:
C:\Program Files\Inkscape\share\extensions

Tutorial

Watch: https://www.youtube.com/watch?v=6b_XMrfLMc0

Transferring G-code to the Machine

Universal Gcode Sender

Download: https://winder.github.io/ugs_website/

Connect & Send

Open UGS, connect to your CNC device, and load the generated .gcode file.

