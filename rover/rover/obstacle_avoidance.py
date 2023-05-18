import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from rclpy.qos import qos_profile_sensor_data, QoSProfile
# qos_profile = QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
#                                           history=rclpy.qos.HistoryPolicy.KEEP_LAST,
#                                           depth=5)

class ObstacleAvoidingBot(Node):
    def __init__(self):
        super().__init__("Go_to_position_node")
        #self.subscription = self.create_subscription(LaserScan, '/scan', self.get_scan_values, 40)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 40)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.get_scan_values, qos_profile_sensor_data)

        time_period = 0.2
        self.timer = self.create_timer(time_period, self.send_cmd_vel)
        self.linear_velocity = 0.22
        self.regions = {'right':[], 'mid':[], 'left':[]}
        self.velocity = Twist()

    def get_scan_values(self, scan_data):
        self.regions = {
            'right': min(min(scan_data.ranges[0:120]), 100),
            'mid': min(min(scan_data.ranges[120:240]), 100),
            'left': min(min(scan_data.ranges[240:360]), 100)
        }

        print(self.regions['left'], '/', self.regions['mid'], '/', self.regions['right'])

    def send_cmd_vel(self):
        self.velocity.linear.x = self.linear_velocity

        if (self.regions['left'] > 4 and self.regions['mid'] > 4 and self.regions['right'] > 4 ):
            self.velocity.angular.z = 0.0   
            print("forward")
        
        elif (self.regions['left'] < 4 and self.regions['mid'] > 4 and self.regions['right'] > 4 ):
            self.velocity.angular.z = -1.57   
            print("turn right") 

        elif (self.regions['left'] > 4 and self.regions['mid'] > 4 and self.regions['right'] < 4 ):
            self.velocity.angular.z = 1.57   
            print("turn left") 
        elif (self.regions['left'] < 4 and self.regions['mid'] < 4 and self.regions['right'] < 4 ):
            self.velocity.angular.z = 3.14 
            self.velocity.linear.x = -self.linear_velocity
            print("turn around") 

        else:
            print("Not implemented")

        self.publisher.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    oab = ObstacleAvoidingBot()
    rclpy.spin(oab)
    rclpy.shutdown()

if __name__=='__main__':
    main()
