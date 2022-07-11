#!/usr/bin/env python3

""" Example for using the SGP30 with ROS2, CircuitPython and the Adafruit library"""
# ROS2
from os import times_result
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Python
import time
import board
import busio
import adafruit_sgp30

class Sensor(Node):

    def __init__(self) -> None:
        # init sensor
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

        # Create library object on our I2C bus
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)

        # Initialize communication with the sensor
        self.sgp30.iaq_init()
        self.sgp30.set_iaq_baseline(0x8973, 0x8a8a)
        self.sgp30.set_iaq_relative_humidity(22.1, 44)

        # Create a publisher for the sensor data
        super().__init__('sensor')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        times_period = 0.5  # seconds
        self.timer = self.create_timer(times_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'eCO2 = %d ppm \t TVOC = %d ppb , Output %d' % (self.sgp30.eCO2, self.sgp30.TVOC, self.i)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sensor = Sensor()

    rclpy.spin(sensor)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    sensor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


