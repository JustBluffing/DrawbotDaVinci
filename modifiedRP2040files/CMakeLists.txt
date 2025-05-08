# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if(EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
cmake_minimum_required(VERSION 3.13)

# Lisäpluginit
option(ADD_HPGL       "Add HPGL plugin"               OFF)
option(ADD_WIFI       "Add WiFi networking"          OFF)
option(ADD_ETHERNET   "Add Ethernet networking"      OFF)
option(ADD_BLUETOOTH  "Add Bluetooth"                OFF)
option(ADD_mDNS       "Add mDNS service"             OFF)
option(ADD_MQTT       "Add MQTT client API"          OFF)
option(ADD_SERVO      "Enable PWM‐servo M280 plugin" ON)  # <--- Tämä

# VSCode Pico‐board setting
set(PICO_BOARD pico CACHE STRING "Board type")

include(pico_sdk_import.cmake)

# Verkko‐pluginien esivalmistelut
if(ADD_WIFI OR ADD_ETHERNET)
    include(networking/CMakeLists.txt)
    include(webui/CMakeLists.txt)
    if(ADD_mDNS OR ADD_MQTT)
        set(LWIP_DIR ${PICO_SDK_PATH}/lib/lwip)
        include(${LWIP_DIR}/src/Filelists.cmake)
    endif()
endif()

# Vakio‐pluginien includet
include(grbl/CMakeLists.txt)
include(fatfs/CMakeLists.txt)
include(motors/CMakeLists.txt)
include(trinamic/CMakeLists.txt)
include(spindle/CMakeLists.txt)
include(sdcard/CMakeLists.txt)
include(keypad/CMakeLists.txt)
include(eeprom/CMakeLists.txt)
include(fans/CMakeLists.txt)
include(bluetooth/CMakeLists.txt)
include(embroidery/CMakeLists.txt)
include(plasma/CMakeLists.txt)
include(laser/CMakeLists.txt)
include(plugins/CMakeLists.txt)
if(ADD_HPGL)
    include(hpgl/CMakeLists.txt)
endif()

project(grblHAL)
pico_sdk_init()

# 1) Luo grblHAL‐suoritettava vain kerran
add_executable(grblHAL
    main.c
    driver.c
    serial.c
    usb_serial.c
    stdio_usb_descriptors.c
    flash.c
    i2c.c
    spi.c
    sr16_out.c
    ioports.c
    ioports_analog.c
    tmc_uart.c
    boards/pico_cnc.c
    boards/btt_skr_pico_10.c
    littlefs/lfs.c
    littlefs/lfs_util.c
    littlefs_hal.c
)

# 2) Jos halutaan mukaan PWM‐servo (M280)
if(ADD_SERVO)
    message(STATUS ">>> PWM_SERVO_M280 plugin INCLUDED <<<")
    # Kerro koodille, että PWM_SERVO_M280‐ominaisuus on päällä
    target_compile_definitions(grblHAL PRIVATE PWM_SERVO_M280=1)
    # Lisää servon ohjauskoodi
    target_sources(grblHAL PRIVATE plugins/pwm_servo_m280.c)
endif()

# 3) Jäljelle jäävät käännös‐ ja generointikutsut
pico_generate_pio_header(grblHAL ${CMAKE_CURRENT_LIST_DIR}/driverPIO.pio)

# RP2040‐ajurit
if(PICO_BOARD STREQUAL "pico" OR PICO_BOARD STREQUAL "pico_w")
    target_compile_definitions(grblHAL PUBLIC RP_MCU=2040)
    if(PICO_SDK_VERSION_STRING VERSION_GREATER_EQUAL "2.1.1")
        target_compile_definitions(grblHAL PUBLIC PICO_USE_FASTEST_SUPPORTED_CLOCK=1)
    endif()
else()
    target_compile_definitions(grblHAL PUBLIC RP_MCU=2350)
endif()
target_compile_definitions(grblHAL PUBLIC RP2040 NEW_FATFS)

# Verkko‐ja Bluetooth‐linkitykset (jos päällä)
if(ADD_WIFI)
    target_compile_definitions(grblHAL PUBLIC WIFI_ENABLE=1 NDEBUG)
    target_sources(grblHAL PRIVATE wifi.c dhcpserver.c)
    target_link_libraries(grblHAL PRIVATE pico_cyw43_arch_lwip_poll)
endif()
if(ADD_ETHERNET)
    target_compile_definitions(grblHAL PUBLIC ETHERNET_ENABLE=1 CYW43_LWIP=0 LWIP_NOASSERT)
    include(networking/wiznet/CMakeLists.txt)
    target_sources(grblHAL PRIVATE w5x00_ll_driver.c)
    target_link_libraries(grblHAL PRIVATE wiznet pico_lwip pico_lwip_nosys)
endif()
if(ADD_WIFI OR ADD_ETHERNET)
    target_compile_definitions(grblHAL PUBLIC WEBUI_AUTO_REPORT_INTERVAL=0)
    if(ADD_mDNS)
        target_compile_definitions(grblHAL PUBLIC LWIP_IGMP=1 LWIP_NUM_NETIF_CLIENT_DATA=1 LWIP_MDNS_RESPONDER=1 MDNS_MAX_SERVICES=8 MDNS_ENABLE=1)
        target_sources(grblHAL PRIVATE ${lwipmdns_SRCS})
    endif()
    if(ADD_MQTT)
        target_compile_definitions(grblHAL PUBLIC MQTT_ENABLE=1)
        target_sources(grblHAL PRIVATE ${lwipmqtt_SRCS})
        target_link_libraries(grblHAL PRIVATE pico_lwip_mqtt)
    endif()
    target_link_libraries(grblHAL PRIVATE networking webui)
endif()
if(ADD_BLUETOOTH)
    target_compile_definitions(grblHAL PUBLIC BLUETOOTH_ENABLE=1 NDEBUG)
    target_sources(grblHAL PRIVATE bt_native.c)
    target_include_directories(grblHAL PRIVATE ${PICO_SDK_PATH}/lib/btstack/src)
    target_link_libraries(grblHAL PRIVATE pico_btstack_classic pico_btstack_ble pico_btstack_cyw43)
    if(NOT ADD_WIFI)
        target_compile_definitions(grblHAL PUBLIC CYW43_LWIP=0)
        target_link_libraries(grblHAL PRIVATE pico_cyw43_arch_poll)
    endif()
endif()

# Linkit ja loput
target_include_directories(grblHAL PRIVATE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(grblHAL PRIVATE
    grbl fatfs sdcard motors trinamic spindle keypad fans laser bluetooth 
    eeprom plasma misc_plugins embroidery tinyusb_device_unmarked
    pico_stdlib pico_unique_id hardware_dma hardware_uart hardware_pio 
    hardware_i2c hardware_spi hardware_gpio hardware_pwm hardware_clocks hardware_flash hardware_rtc
)
pico_add_extra_outputs(grblHAL)

# Puhdistetaan cache‐muuttujat
unset(PICO_BOARD CACHE)
unset(ADD_WIFI CACHE)
unset(ADD_ETHERNET CACHE)
unset(ADD_BLUETOOTH CACHE)
unset(ADD_HPGL CACHE)
unset(ADD_mDNS CACHE)
unset(ADD_MQTT CACHE)
unset(ADD_SERVO CACHE)
