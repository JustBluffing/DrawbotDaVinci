/*
  pwm_servo_m280.c - plugin for M280, Marlin style servo commands

  grblHAL misc. plugin
  Generates a 50 Hz hardware-PWM on GPIO15 for M280 commands.
*/
#include "pico/stdlib.h"
#include "hardware/clocks.h"
#include "hardware/gpio.h"
#include "hardware/pwm.h"
#include "driver.h"


#if PWM_SERVO_ENABLE == 1

#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include "grbl/hal.h"
#include "grbl/protocol.h"
#include "grbl/ioports.h"

#define SERVO_GPIO_PIN      15
#define SERVO_PWM_WRAP      10000u    // PWM-levels: 0…10000
#define SERVO_PWM_FREQ_HZ   50.0f     // Desired frequency

#ifndef N_PWM_SERVOS
#define N_PWM_SERVOS 1
#endif
#if N_PWM_SERVOS > 4
#undef N_PWM_SERVOS
#define N_PWM_SERVOS 4
#endif

#define DEFAULT_MIN_ANGLE 0.0f
#define DEFAULT_MAX_ANGLE 180.0f

typedef struct {
    float min_angle, max_angle;
    float angle;
} servo_t;

static user_mcode_ptrs_t   user_mcode;
static on_report_options_ptr on_report_options;
static uint8_t             n_servos = 0;
static servo_t             servos[N_PWM_SERVOS];

// Set servo angle in degrees -> PWM level
static bool pwm_servo_set_angle(uint8_t servo, float angle)
{
    if(servo >= n_servos) return false;
    servos[servo].angle = angle;
    // Map [min…max] → [0…WRAP]
    uint32_t level = (uint32_t)(
        (angle - servos[servo].min_angle)
        / (servos[servo].max_angle - servos[servo].min_angle)
        * SERVO_PWM_WRAP
    );
    pwm_set_gpio_level(SERVO_GPIO_PIN, level);
    return true;
}

static float pwm_servo_get_angle(uint8_t servo)
{
    return (servo < n_servos) ? servos[servo].angle : -1.0f;
}

static user_mcode_type_t mcode_check(user_mcode_t mcode)
{
    return (mcode == PWMServo_SetPosition) ? UserMCode_Normal
         : user_mcode.check ? user_mcode.check(mcode)
                            : UserMCode_Unsupported;
}

static status_code_t mcode_validate(parser_block_t *gc_block)
{
    if(gc_block->user_mcode != PWMServo_SetPosition)
        return user_mcode.validate ? user_mcode.validate(gc_block)
                                   : Status_Unhandled;

    // Validate P- and S-words
    if(gc_block->words.p && (!isintf(gc_block->values.p)
       || (uint8_t)gc_block->values.p >= n_servos))
        return Status_GcodeValueOutOfRange;

    if(gc_block->words.s) {
        float s = gc_block->values.s;
        float mn = servos[(uint32_t)gc_block->values.p].min_angle,
              mx = servos[(uint32_t)gc_block->values.p].max_angle;
        if(s < mn || s > mx)
            return Status_GcodeValueOutOfRange;
    }

    // Input accepted
    gc_block->words.p = gc_block->words.s = Off;
    return Status_OK;
}

static void mcode_execute(uint_fast16_t state, parser_block_t *gc_block)
{
    if(gc_block->user_mcode != PWMServo_SetPosition) {
        if(user_mcode.execute) user_mcode.execute(state, gc_block);
        return;
    }

    uint8_t id = (uint8_t)gc_block->values.p;
    if(gc_block->words.s) {
        pwm_servo_set_angle(id, gc_block->values.s);
    } else {
        // Report
        char buf[64];
        float v = pwm_servo_get_angle(id);
        snprintf(buf, sizeof(buf), "[Servo %u position: %.2f degrees]" ASCII_EOL, id, v);
        hal.stream.write(buf);
    }
}

static void onReportOptions(bool newopt)
{
    on_report_options(newopt);
    if(!newopt) report_plugin("PWM servo", "0.05");
}

void pwm_servo_init(void)
{
    // Copy original callbacks 
    memcpy(&user_mcode, &grbl.user_mcode, sizeof(user_mcode_ptrs_t));
    // Replace with our own
    grbl.user_mcode.check    = mcode_check;
    grbl.user_mcode.validate = mcode_validate;
    grbl.user_mcode.execute  = mcode_execute;
    // Tag plugin reporting
    on_report_options = grbl.on_report_options;
    grbl.on_report_options = onReportOptions;

    // Initialize servo data
    n_servos = N_PWM_SERVOS;
    for(uint8_t i = 0; i < n_servos; i++) {
        servos[i].min_angle = DEFAULT_MIN_ANGLE;
        servos[i].max_angle = DEFAULT_MAX_ANGLE;
        servos[i].angle     = 0.0f;
    }
// --- Configure GPIO15 as hardware-PWM 50 Hz ---
gpio_set_function(SERVO_GPIO_PIN, GPIO_FUNC_PWM); {
    uint slice = pwm_gpio_to_slice_num(SERVO_GPIO_PIN);
    pwm_config cfg = pwm_get_default_config();
    pwm_config_set_wrap(&cfg, SERVO_PWM_WRAP);
    float sys_hz = (float)clock_get_hz(clk_sys);
    pwm_config_set_clkdiv(&cfg, sys_hz / (SERVO_PWM_WRAP * SERVO_PWM_FREQ_HZ));
    pwm_init(slice, &cfg, true);
}    
}

#endif // PWM_SERVO_ENABLE
