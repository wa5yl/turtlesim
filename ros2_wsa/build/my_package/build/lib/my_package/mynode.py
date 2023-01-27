#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # ROS2 package to convert between ROS and OpenCV Images
import cv2 # Python OpenCV library
import numpy as np
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class Controller(Node):
    def __init__(self):
        super().__init__("cmd_vel_publisher")
        self.window_name = "Controller"
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.create_window, 10)
        self.get_logger().info("Turtlesim Controller initiated")
        self.point = None
        self.rectanlge_size = 100
        self.window_size = np.zeros((512,700,3), np.uint8)
                

    def create_window(self, image_data):
        cv_image = np.zeros((512,700,3), np.uint8)
        if(self.point is not None):
            cv2.rectangle(cv_image,( self.point[0]-50,
                                     self.point[1]-50 ),
                                   ( self.point[0]+50,
                                     self.point[1]+50 ),
                                   ( 0,255,0 ),
                                    3 )
        cv2.imshow(self.window_name, cv_image)
        cv2.waitKey(25)
        cv2.setMouseCallback(self.window_name, self.draw_rectangle)


    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN: # check if mouse event is click
            self.point = (x,y)
            self.click_callback()


    def click_callback(self):
        msg = Twist()
        
        if self.point[1] < (self.window_size.shape[0]/2) and self.point[0] > (self.window_size.shape[1]*0.5):
            msg.linear.x = 1.0
        elif self.point[1] >= (self.window_size.shape[0]/2) and self.point[0] > (self.window_size.shape[1]*0.5):
            msg.linear.x = -1.0
        elif self.point[1] >= (self.window_size.shape[0]/2) and self.point[0] < (self.window_size.shape[1]*0.5):
            msg.angular.z = 0.5
        elif self.point[1] < (self.window_size.shape[0]/2) and self.point[0] < (self.window_size.shape[1]*0.5):
            msg.angular.z = -0.5
        
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Controller()
    rclpy.spin(minimal_publisher)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
