/*
  pico_cnc.c - driver code for RP2040 ARM processors

  Part of grblHAL

  Copyright (c) 2021-2025 Terje Io
  
  grblHAL is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  grblHAL is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with grblHAL. If not, see <http://www.gnu.org/licenses/>.
*/

#include "driver.h"

#include "hardware/clocks.h"
#include "hardware/pwm.h"
#include "hardware/gpio.h"

#if defined(BOARD_PICO_CNC)


void board_init (void)
{

#if PWM_SERVO_ENABLE
    {
        // Logical Port_Analog port 0
        uint8_t servo_port = 0;  
        // Tell grblHAL that port 0 is an output
        ioport_claim(Port_Analog, Port_Output, &servo_port, "PWM Servo");

    }

     // 2) Configure GPIO15 as hardware-PWM at 50 Hz
     const uint PIN    = 15;
     const uint32_t WRAP = 10000;            // resolution steps (0…10000)
     const float    FREQ = 50.0f;            // desired 50 Hz
 
     // a) Set the GPIO function to PWM
     gpio_set_function(PIN, GPIO_FUNC_PWM);
 
     // b) Figure out which PWM slice it is
     uint slice = pwm_gpio_to_slice_num(PIN);
 
     // c) Get default config, set wrap and clkdiv for 50 Hz
     pwm_config cfg = pwm_get_default_config();
     pwm_config_set_wrap(&cfg, WRAP);
     float sys_hz = (float)clock_get_hz(clk_sys);
     pwm_config_set_clkdiv(&cfg, sys_hz / (WRAP * FREQ));
 
     // d) Initialize and enable the slice
     pwm_init(slice, &cfg, true);
 #endif  // PWM_SERVO_ENABLE
 
    // If you need other I/O ports (e.g. step, direction, etc.),
    // they are claimed here in board_init() as before.
 }
 
 #endif // defined(BOARD_PICO_CNC)
