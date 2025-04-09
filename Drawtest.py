from machine import Pin,PWM
import time
import _thread

servo_pin = Pin(15, Pin.OUT)
dir_pin_x = Pin(16, Pin.OUT)
step_pin_x = Pin(17, Pin.OUT)

dir_pin_y = Pin(18, Pin.OUT)
step_pin_y = Pin(19, Pin.OUT)

step_multiplier = 1
step_speed = 1000

# Rotates the X-axis motor.
# Time in microseconds.
def step_x(steps, direction, rotating_time):
    dir_pin_x.value(direction)
    for step in range(steps):
        step_pin_x.value(not step_pin_x.value())
        time.sleep_us(rotating_time)
        
def step_y(steps, direction, rotating_time):
    dir_pin_y.value(direction)
    for step in range(steps):
        step_pin_y.value(not step_pin_y.value())
        time.sleep_us(rotating_time)

def lift_pen():
    servo = PWM(servo_pin)
    servo.freq(50)
    lift_angle = 70
    write_val = 6400/180*angle + 1900
    servo.duty_u16(int(write_val))
    
def set_pen():
    servo = PWM(servo_pin)
    servo.freq(50)
    lift_angle = 80
    write_val = 6400/180*angle + 1900
    servo.duty_u16(int(write_val))
    
# Calculates the amount of steps for each axis.
# start and end are tuples of x and y coordinates.
def calculate_steps(start, end):
    dist_x = abs(end[0]-start[0])
    dist_y = abs(end[1]-start[1])
    distance = (dist_x**2+dist_y**2)**(1/2)
    steps_x = int(dist_x*step_multiplier)
    steps_y = int(dist_y*step_multiplier)
    
    return steps_x,steps_y

# Calculates how much faster the motor with more steps to do needs to rotate to reach the end at the same time.
def calculate_time_multiplier(steps_x, steps_y):
    step_time_multiplier = min(steps_x,steps_y)/max(steps_x,steps_y)
    return step_time_multiplier

# Draws a line from starting coordinates to end.
# Coordinates as a tuple.
def draw(start, end):
    steps_x,steps_y = calculate_steps(start, end)
    time_multiplier = calculate_time_multiplier(steps_x, steps_y)
    
    # Set the rotation direction
    if end[0]-start[0] < 0:
        dir_x = 0
    else:
        dir_x = 1
    if end[1]-start[1] < 0:
        dir_y = 0
    else:
        dir_y = 1
        
    if steps_x < steps_y:
        time_x = step_speed
        time_y = int(step_speed*time_multiplier)
    else:
        time_x = int(step_speed*time_multiplier)
        time_y = step_speed
        
    _thread.start_new_thread(step_y, (steps_y, dir_y, time_y))
    step_x(steps_x, dir_x, time_x)


def draw_test(start, end):
    draw((100,100),(8000,8000))

draw_test((100,100),(5000,3000))

#step_x(5000, 1, 2000)
