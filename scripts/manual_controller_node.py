#!/usr/bin/env python
# -*- coding: utf8 -*-#

import rospy
import traceback
from keyboard.msg import Key
from geometry_msgs.msg import Twist
from isr_m2_driver.srv import *

twist = Twist()
twist.linear.x = 0
twist.angular.z = 0

def inc_linear_vel(arg):
    twist.linear.x += arg
    global pub
    pub.publish(twist)

def inc_angular_vel(arg):
    twist.angular.z += arg
    global pub
    pub.publish(twist)

def reset_vel(arg):
    twist.linear.x = 0
    twist.angular.z = 0
    global pub
    pub.publish(twist)

def enable_motor(arg):
    rospy.wait_for_service('robot_command')
    try:
        req = RobotCommandRequest()
        req.command = RobotCommandRequest.COMMAND_ENABLE_MOTOR
        req.arg1 = arg
        service_proc = rospy.ServiceProxy('robot_command', RobotCommand)
        res = service_proc(req)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

HANDLER_MAP = {
    Key.KEY_UP:    [inc_linear_vel,  0.01],
    Key.KEY_DOWN:  [inc_linear_vel, -0.01],
    Key.KEY_LEFT:  [inc_angular_vel, 0.1],
    Key.KEY_RIGHT: [inc_angular_vel, -0.1],
    Key.KEY_SPACE: [reset_vel, 0],
    #Key.KEY_i:     [initialize_robot, 0],
    Key.KEY_e:     [enable_motor, 1],
    Key.KEY_d:     [enable_motor, 0],
    #Key.KEY_t:     [stop_motor, 1],
    #Key.KEY_r:     [stop_motor, 0],
    #Key.KEY_v:     [read_velocity, 0],
    #Key.KEY_p:     [reset_robot_pos, 0],
    #Key.KEY_s:     [read_robot_status, 0],
}

def key_callback(data):
    try:
        HANDLER_MAP[data.code][0](HANDLER_MAP[data.code][1])
    except:
        traceback.print_exc()

def print_instruction():
    print "Forward/back arrows: linear velocity incr/decr"
    print "-----------------------------------------------"

def manual_controller():
    print_instruction()
    global pub
    pub = rospy.Publisher('cmd_vel', Twist)
    rospy.Subscriber('keyboard_node/keydown', Key, key_callback)
    rospy.init_node('isr_m2_manual_controller_node')
    rospy.spin()

if __name__ == '__main__':
    manual_controller()
