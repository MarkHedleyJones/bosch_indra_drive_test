#!/usr/bin/env python
from sensor_msgs.msg import Joy
from bosch_indra_driver.msg import IndraControl
from bosch_indra_driver.msg import IndraStatus
import rospy
import math
import sys

app = {
    'device_ready': None,
    'toggle': None,
    'publisher': None
}

app['pub'] = rospy.Publisher('/indra_command', IndraControl, queue_size=1)

def cb_indra(msg):
    if msg.ready_for_command is True:
        if app['device_ready'] == False:
            print("Device is now ready for next command.")
            sys.stdout.write("\033[F")
            app['device_ready'] = True
    else:
        app['device_ready'] = False


def cb_joystick(msg):
    out = IndraControl()
    if 1 in msg.buttons:
        print("Moving to next position...           ")
        sys.stdout.write("\033[F")
        if app['toggle']:
            out.position_command = 1800000   # Move forward 180 degrees
            out.velocity_command = 1000000
            app['toggle'] = False
        else:
            out.position_command = -1800000  # Move backward 180 degrees
            out.velocity_command = -1000000
            app['toggle'] = True
        app['pub'].publish(out)


def main():
    rospy.init_node('bosch_indra_drive_test', anonymous=True)
    app['device_ready'] = False
    app['toggle'] = False
    sub1 = rospy.Subscriber('/indra_status', IndraStatus, cb_indra)
    sub2 = rospy.Subscriber('/joy', Joy, cb_joystick)
    rospy.spin()


if __name__ == '__main__':
    main()