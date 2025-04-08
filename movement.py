"""
This piece of code gets the motor to rotate smoothly. 12V and 1A limits.
"""

from machine import Pin
import time

dir_pin = Pin(16, Pin.OUT)
step_pin = Pin(17, Pin.OUT)

def step_motor(steps, direction):
    dir_pin.value(direction)
    for step in range(steps):
        step_pin.value(1)
        time.sleep_us(1000)
        step_pin.value(0)
        time.sleep_us(1000)
        
step_motor(4000,0)
