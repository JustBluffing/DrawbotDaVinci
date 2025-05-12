This repository contains configuration and build instructions for compiling **grblHAL** for the RP2040 (Raspberry Pi Pico) using ARM GCC, CMake, and Ninja, and producing `.uf2` firmware images.


---
## Prerequisites 
1. ARM GCC Toolchain
   Download and install [ARM GNU Toolchain](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads) (e.g. `arm-none-eabi-gcc`)
2. CMake
   Install via your package manager or from https://cmake.org/download/
3. Ninja
   Install via your package manager or from https://ninja-build.org/.  
4. Pico SDK
```bash
   cd ~
   git clone https://github.com/raspberrypi/pico-sdk.git
   cd pico-sdk
   git checkout sdk-<version>  # e.g. sdk-1.5.0

---

## Environment Setup

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PICO_SDK_PATH=~/pico-sdk
export PATH="$PATH:/path/to/arm-none-eabi/bin"


## grblHAL RP2040

Clone grblHAL RP2040

git clone https://github.com/<your-org>/grblHAL-rp2040.git
cd grblHAL-rp2040

You need to overwrite the following files found in DrawbotDaVinci/modifiedRO2040files from the RP2040. Additionally you have to create settings.json file
to .vscode subfolder in RP2040.  

After that you can use Visual Studio Code to cofigure and build new .uf2 files using CMake. 


Latest working firmware is the grblHAL.uf2 file found in the main page of DrawbotDaVinci




Images to gcode

## Software options

1. Inkscape
   Download Inkscape https://inkscape.org
   Gcodetools extension
      https://github.com/kliment/gcodetools
      
      Copy the gcodetools folder (and its .inx/.py files) into the extensions directory
(C:\ProgramFiles\Inkscape\share\extensions)

   Tutorial on how to use gcodetools extension
   https://www.youtube.com/watch?v=6b_XMrfLMc0





Transferring gcode to the machine

Download Universal Gcode Sender https://winder.github.io/ugs_website/



