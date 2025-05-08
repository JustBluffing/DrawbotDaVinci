
/*
  generic_map.h - driver code for RP2040 ARM processors

  Part of grblHAL

  Copyright (c) 2021-2025 Terje Io
  Copyright (c) 2021 Volksolive

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

#if TRINAMIC_ENABLE
#error Trinamic plugin not supported!
#endif

#if N_ABC_MOTORS
#error "Axis configuration is not supported!"
#endif

#if I2C_STROBE_ENABLE && MOTOR_FAULT_ENABLE
#error "Motor fault input and I2C strobe input (keypad plugin) cannot be enabled at the same time."
#endif

// Define step pulse output pins.
#define STEP_PORT               GPIO_PIO  // N_AXIS pin PIO SM
#define STEP_PINS_BASE          2         // N_AXIS number of consecutive pins are used by PIO

// Define step direction output pins.
#define DIRECTION_PORT          GPIO_OUTPUT
#define X_DIRECTION_PIN         13
#define Y_DIRECTION_PIN         12
#define Z_DIRECTION_PIN         26
#define DIRECTION_OUTMODE       GPIO_MAP

// Define stepper driver enable/disable output pin.
#define ENABLE_PORT             GPIO_OUTPUT
#define STEPPERS_ENABLE_PIN     8

// Define homing/hard limit switch input pins.
#define X_LIMIT_PIN             26             
#define Y_LIMIT_PIN             26
#define Z_LIMIT_PIN             26
#define LIMIT_INMODE            GPIO_MAP

// Define auxiliary I/O
#define AUXINPUT0_PIN           22
#define AUXINPUT1_PIN           21
#define AUXINPUT2_PIN           28 // Probe


#define AUXOUTPUT1_PORT         GPIO_OUTPUT
#define AUXOUTPUT1_PIN          11
#define AUXOUTPUT2_PORT         GPIO_OUTPUT
#define AUXOUTPUT2_PIN          17
#define AUXOUTPUT3_PORT         GPIO_OUTPUT
#define AUXOUTPUT3_PIN          18
#define AUXOUTPUT4_PORT         GPIO_OUTPUT
#define AUXOUTPUT4_PIN          10
#define AUXOUTPUT5_PORT         GPIO_OUTPUT
#define AUXOUTPUT5_PIN          26
#define AUXOUTPUT6_PORT         GPIO_OUTPUT // Coolant flood
#define AUXOUTPUT6_PIN          20   
#define AUXOUTPUT7_PORT         GPIO_OUTPUT // Coolant mist
#define AUXOUTPUT7_PIN          26  

// servo controls for M280 pen-servo plugin
#define HAS_IOPORTS
#define SERVO

// Tämä aktivoi pwm_servo_m280.c:n:
#define PWM_SERVO_ENABLE   1
#define N_PWM_SERVOS       1

//#define AUXOUTPUT0_PWM_PORT GPIO_OUTPUT
//#define AUXOUTPUT0_PWM_PIN 15


#define PEN_SERVO_PORT     Port_Analog
#define PEN_SERVO_PIN      0

//#define NEOPIXELS_PIN 27
//#define NEOPIXELS_NUM 5
//Define user-control controls (cycle start, reset, feed hold) input pins.

// Define driver spindle pins
#if DRIVER_SPINDLE_ENABLE
#define SPINDLE_PORT            GPIO_OUTPUT
#endif
#if DRIVER_SPINDLE_ENABLE & SPINDLE_PWM
#define SPINDLE_PWM_PIN         AUXOUTPUT7_PIN
#endif
#if DRIVER_SPINDLE_ENABLE & SPINDLE_DIR
#define SPINDLE_DIRECTION_PIN   AUXOUTPUT6_PIN
#endif
#if DRIVER_SPINDLE_ENABLE & SPINDLE_ENA   
#define SPINDLE_ENABLE_PIN      AUXOUTPUT6_PIN
#endif

// Define flood and mist coolant enable output pins.
#if COOLANT_ENABLE
#define COOLANT_PORT            GPIO_OUTPUT
#endif
#if COOLANT_ENABLE & COOLANT_FLOOD
#define COOLANT_FLOOD_PIN       AUXOUTPUT6_PIN
#endif
#if COOLANT_ENABLE & COOLANT_MIST
#define COOLANT_MIST_PIN        AUXOUTPUT7_PIN
#endif

// Define user-control controls (cycle start, reset, feed hold) input pins.
#undef RESET_PIN               
#undef FEED_HOLD_PIN           
#undef CYCLE_START_PIN         

#if PROBE_ENABLE
#define PROBE_PIN               AUXINPUT2_PIN
#endif

#if SAFETY_DOOR_ENABLE
#define SAFETY_DOOR_PIN         AUXINPUT1_PIN
#endif

#if I2C_STROBE_ENABLE
#define I2C_STROBE_PIN          AUXINPUT0_PIN
#elif MOTOR_FAULT_ENABLE
#define MOTOR_FAULT_PIN         AUXINPUT0_PIN
#endif
