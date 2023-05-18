import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class follow_wall_bot(Node):
    def __init__(self):
        super().__init__('Go_to_position_node')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.get_scan_values, qos_profile_sensor_data)

        time_period = 0.2
        self.timer = self.create_timer(time_period, self.send_cmd_vel)
        self.velocity = Twist()
        self.region1 = 0 ; self.region2 = 0 ; self.region3 = 0
        self.linear_vel = 0.2
        self.error = 0
        self.case = " "

    def get_scan_values(self, scan_data):
        self.region1 = min(min(scan_data.ranges[0:20]),100)
        self.region2 = min(min(scan_data.ranges[20:40]),100)
        self.region3 = min(min(scan_data.ranges[40:60]),100)
        
        print(round(self.region3, 3), '/', round(self.region2, 3), '/', round(self.region1, 3), self.error, self.case)
    
    def proportional_controller(self):
        self.error = 1.2 - self.region1
        if self.error < -1.57:
            self.error = -1.57

        self.velocity.linear.x = self.linear_vel
        self.velocity.angular.z = self.error

    def send_cmd_vel(self):
        if self.region1 < 4:
            self.case = "basic"
            self.proportional_controller()
        if self.region2  > 4 and self.region3  > 4:
            self.case = "Turn"
            self.velocity.linear.x = 0.4
            self.velocity.angular.z = -1.57

        self.publisher.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    fwb = follow_wall_bot()
    rclpy.spin(fwb)
    rclpy.shutdown()

if __name__ == '__main__':
    main()