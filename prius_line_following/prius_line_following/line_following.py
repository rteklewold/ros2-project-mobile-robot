import rclpy
import cv2
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from rclpy.qos import qos_profile_sensor_data
from cv_bridge import CvBridge


class line_detection_and_following(Node):
    def __init__(self):
        super().__init__('Lane_follower')
        self.subscriber = self.create_subscription(Image, '/camera/image_raw', self.process_data, qos_profile_sensor_data)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 40)
        time_period = 0.2 ; self.timer = self.create_timer(time_period, self.send_cmd_velocity)
        self.velocity = Twist()
        self.error = 0
        self.action = " "
        self.cvbridge = CvBridge()
    
    def send_cmd_velocity(self):
        self.velocity.linear.x = 0.5

        if self.error > 0:
            self.velocity.angular.z = 0.15
            self.action = "Go left"
        else:
           self.velocity.angular.z = -0.15 
           self.action = "Go right"
        self.publisher.publish(self.velocity)

 
    def process_data(self, data):
        frame = self.cvbridge.imgmsg_to_cv2(data)
        light_line = np.array([100, 100, 100])
        dark_line = np.array([200, 200, 200])
        mask = cv2.inRange(frame, light_line, dark_line)
        canny = cv2.Canny(mask, 10, 40)
        r1 = 150 ; c1 = 0
        img = canny[r1:r1+240, c1:c1+640]

        edge = []
        for i in range(639):
            if img[160, i] == 255:
                edge.append(i)
        print(edge)

        if len(edge) == 4:
            edge[0] = edge[0]
            edge[1] = edge[3]

        if len(edge) == 3:
            if edge[1] - edge[0] >5 :
                edge[0] = edge[0]
                edge[1] = edge[1]
            else:
                edge[0] = edge[0]
                edge[1] = edge[2]
        if len(edge) < 2:
            edge = [240, 440]

        mid_length = edge[1] - edge[0]
        mid_pt = edge[0] + mid_length/2

        img[160, int(mid_pt)] = 255

        frame_mid = 639/2
        self.error = frame_mid - mid_pt

        img[160, int(frame_mid)] = 255    
        img[159, int(frame_mid)] = 255 
        img[161, int(frame_mid)] = 255 

        f_img = cv2.putText(img, self.action, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0), 2)

        cv2.imshow('output image', f_img)
        cv2.waitKey(1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(args = None):
    rclpy.init(args=args)
    lane_follower = line_detection_and_following()
    rclpy.spin(lane_follower)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


   
    