import rospy
import Queue

from mg_msgs.msg import PVATrajectory
from mg_msgs.msg import PVA_Stamped

class Node:
    def __init__(self, trajectory_queue):
        self.__trajectory_queue = trajectory_queue

        rospy.init_node('trajectory_generator')
        self.__trajectory_publisher = rospy.Publisher('trajectory', PVATrajectory, queue_size=1)

    def Run(self):
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():

            # If there is a trajectory in the queue, publish it
            try:
                numpy_trajectory = self.__trajectory_queue.get(False)
                self.__publish_pva_trajectory(numpy_trajectory)
            except Queue.Empty:
                # Do nothing
                pass

            # Rate limit
            rate.sleep()

    def __publish_pva_trajectory(self, numpy_trajectory):
        """
        Takes a numpy matrix and publishes a PVATrajectory message. Expects a time-ordered matrix of the following form:
        [x, y, z, yaw, vel_x, vel_y, vel_z, acc_x, acc_y, acc_z]^T
        with time increasing as a column value
        """
        for pva in numpy_trajectory.T:
            print(pva.shape)
