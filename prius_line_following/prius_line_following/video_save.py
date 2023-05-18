import rclpy
import cv2
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import qos_profile_sensor_data


class Video_get(Node):
    def __init__(self):
        super().__init__('video_subscriber')
        self.subscriber = self.create_subscription(Image, '/camera/image_raw', self.process_data, qos_profile_sensor_data)
        self.out = cv2.VideoWriter('/home/ecn/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (640, 480))
        self.bridge = CvBridge()

    def process_data(self, data):
        frame = self.bridge.imgmsg_to_cv2(data)
        self.out.write(frame)
        cv2.imshow("output", frame)
        cv2.imwrite('/home/ecn/output.png', frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    image_subsciber =  Video_get()
    rclpy.spin(image_subsciber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
