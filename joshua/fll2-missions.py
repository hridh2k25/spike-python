from hub import light_matrix, port, motion_sensor, power_off
import motor
import runloop
import math
import motor_pair
from math import *
import hub
#functions
#forward(centimeters,speed) and bacwards(centimeters,speed)
#turn_right(deegres) and turn_left(deegres) cannot go over 355 deegrees in one turn
#arm_up(deegres) and arm_down(deegres)
#
#
#
WHEEL_CIRCUMFERENCE = 27.4
DISTANCE_BETWEEN_WHEELS = 11.4 #cm - please measure your own robot.
#ports underneath
motor_pair.pair(motor_pair.PAIR_1, port.A, port.C)
drive_motor_pair = motor_pair.PAIR_1
default_velocity = 30
turn_velocity= 100
LEFT_ARM_MOTOR=port.B
RIGHT_MOTOR=port.D

# input must be in the same unit as WHEEL_CIRCUMFERENCE
def convert_distance_to_degree(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

# input must be in the same unit as WHEEL_CIRCUMFERENCE
def backward(distance_cm, speed=360):
        degrees = convert_distance_to_degree(abs(distance_cm)*-1)
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0, velocity=speed)


def move_for_distance(distance_cm):
        degrees = convert_distance_to_degree(abs(distance_cm))
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0)

def forward(distance_cm, speed=360):
        degrees = convert_distance_to_degree(distance_cm)
        return motor_pair.move_for_degrees(drive_motor_pair,degrees,0, velocity=speed)


PIVOT_CIRCUMFERENCE = 2 * DISTANCE_BETWEEN_WHEELS * math.pi
async def pivot_turn(robot_degrees, motor_speed=turn_velocity):
    # Add a multiplier for gear ratios if you’re using gears
    motor_degrees = int((PIVOT_CIRCUMFERENCE/WHEEL_CIRCUMFERENCE) * abs(robot_degrees))
    if robot_degrees > 0:
        # pivot clockwise
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, 50, velocity=motor_speed)
    else:
        #pivot counter clockwise
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, motor_degrees, -50, velocity=motor_speed)

# Function that returns true when the absolute yaw angle is 90 degrees
def turn_done():
    # convert tuple decidegree into same format as in app and blocks
    return abs(motion_sensor.tilt_angles()[0] * -0.1) > 90



async def spin_turn(degrees):
    if abs(degrees) > 355: #cannot be used over 355 degrees
        print("Out of range")
        return
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    global degrees_to_turn, stop_angle
    degrees_to_turn = degrees # set the global to use in the turn_done function
    # set the stop_angle global to use in the turn_done function
    if (abs(degrees) < 180):
        stop_angle = abs(degrees_to_turn)
    else:
        stop_angle = (360 - abs(degrees)) if degrees < 0 else (abs(degrees) - 360)
    # set the steering laue based on turn direction
    steering_val = 100 if degrees >= 0 else -100
    motor_pair.move(motor_pair.PAIR_1, steering_val, velocity=200)
    await runloop.until(turn_done)
    motor_pair.stop(motor_pair.PAIR_1)

async def turn_left(degrees):
    await spin_turn(abs(degrees))

async def turn_right(degrees):
    await spin_turn(abs(degrees)*-1 )

async def arm_up(degrees:int,velocity=360):
    await motor.run_for_degrees(LEFT_ARM_MOTOR, (abs(degrees)*2), velocity)

async def arm_down(degrees:int,velocity=360):
    await motor.run_for_degrees(LEFT_ARM_MOTOR, abs(degrees)*2*-1, velocity)

async def arm_right(degrees:int,velocity=360):
    await motor.run_for_degrees(RIGHT_MOTOR, abs(degrees), velocity)

async def arm_left(degrees:int,velocity=360):
    await motor.run_for_degrees(RIGHT_MOTOR, (abs(degrees)*-1), velocity)

async def reset_motor_position(port,degree=0, velocity=360):
    await motor.run_to_absolute_position(port,degree,velocity)
    


#start on the 5.75 squares from the left
async def missions1and2():
    await arm_down(90)
    await forward(76,1000)
    await arm_up(90)
    await backward(75,1000)

async def boulder_mission():
    await forward(65, 700)
    await arm_left(90)
    await backward(65, 700)

async def marketplace_flippy_and_boulder_mission():
    await forward(68,700)
    await runloop.sleep_ms(100)
    await turn_right(35)
    await arm_left(70)
    await backward(71,700)




runloop.run(())
