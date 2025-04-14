from machine import Pin,PWM
import time
import _thread

servo_pin = Pin(15, Pin.OUT)
dir_pin_x = Pin(16, Pin.OUT)
step_pin_x = Pin(17, Pin.OUT)
M0_pin_x = Pin(10, Pin.OUT)
M1_pin_x = Pin(11, Pin.OUT)
dir_pin_y = Pin(18, Pin.OUT)
step_pin_y = Pin(19, Pin.OUT)
M0_pin_y = Pin(12, Pin.OUT)
M1_pin_y = Pin(13, Pin.OUT)

step_multiplier = 1
step_speed = 1000

# Set microstep mode
# Could require different current settings?

def set_step_mode(axis, mode):
    if axis == "x":
        M0 = M0_pin_x
        M1 = M1_pin_x
    else:
        M0 = M0_pin_y
        M1 = M1_pin_y
    if mode == "full":
        M0.value(0)
        M1.value(0)
    elif mode == "half":
        M0.value(1)
        M1.value(0)
    elif mode == "quarter":
        M0.value(0)
        M1.value(1)
    elif mode == "eighth":
        M0.value(1)
        M1.value(1)
    print(f"Set mode for the {axis} axis motor to {mode}")
    

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
    lift_angle = 50
    write_val = 6400/180*lift_angle + 1900
    servo.duty_u16(int(write_val))
    
def set_pen():
    servo = PWM(servo_pin)
    servo.freq(50)
    lift_angle = 70
    write_val = 6400/180*lift_angle + 1900
    servo.duty_u16(int(write_val))
    
# Saves the location of the pen.
# Coordinates as a tuple (x, y)
def save_pen_location(coordinates):
    # Binary file faster if more locations
    pen_data = open("pen_data.txt", "w")
    pen_data.write(str(coordinates))
    pen_data.close()
    
def read_pen_location():
    pen_data = open("pen_data.txt")
    pen_location_str = pen_data.read()
    pen_location = tuple(map(int, pen_location_str.strip("()").split(",")))
    pen_data.close()
    return pen_location
    
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
        speed_x = step_speed
        speed_y = int(step_speed*time_multiplier)
    else:
        speed_x = int(step_speed*time_multiplier)
        speed_y = step_speed

    # Expect something before setting global variable?
    print(f"Rotating x axis motor at speed {speed_x} µs/step into direction {dir_x} for {steps_x} steps")
    print(f"Rotating y axis motor at speed {speed_y} µs/step into direction {dir_y} for {steps_y} steps")
    _thread.start_new_thread(step_y, (steps_y, dir_y, speed_y))
    step_x(steps_x, dir_x, speed_x)
    
    global pen_location
    pen_location = end


def draw_test(start, end):
    set_step_mode("x", "eighth")
    set_step_mode("y", "eighth")
    draw(start,end)

draw_test((0,0),(2000,4000))
#set_pen()

#step_x(5000, 1, 2000)
