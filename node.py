import rospy
import Queue
import tf

from mg_msgs.msg import PVATrajectory
from mg_msgs.msg import PVA_Stamped

class Node:
    def __init__(self, trajectory_queue):
        self.__trajectory_queue = trajectory_queue

        rospy.init_node('trajectory_generator')
        self.__trajectory_publisher = rospy.Publisher('/phoenix/trajectory', PVATrajectory, queue_size=1)

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
        pva_trajectory= PVATrajectory()

        for pva in numpy_trajectory.T:
            pva_msg = PVA_Stamped()

            pva_msg.pos.position.x = pva[0]
            pva_msg.pos.position.y = pva[1]
            pva_msg.pos.position.z = pva[2]

            # Build quaternion from yaw
            roll, pitch, yaw = 0, 0, pva[3]
            q = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
            pva_msg.pos.orientation.x = q[0]
            pva_msg.pos.orientation.y = q[1]
            pva_msg.pos.orientation.z = q[2]
            pva_msg.pos.orientation.w = q[3]

            pva_msg.vel.linear.x = pva[4]
            pva_msg.vel.linear.y = pva[5]
            pva_msg.vel.linear.z = pva[6]

            pva_msg.acc.linear.x = pva[7]
            pva_msg.acc.linear.y = pva[8]
            pva_msg.acc.linear.z = pva[9]

            pva_trajectory.pva.append(pva_msg)

        self.__trajectory_publisher.publish(pva_trajectory)


