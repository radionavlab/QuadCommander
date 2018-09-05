#!/usr/bin/python2

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
import jsonpickle.ext.numpy as jp_numpy
import threading
import rospy
from Queue import Queue

from application import Application
from node        import Node

def main():
    # Configure the json numpy handlers
    jp_numpy.register_handlers()

    # Create trajectory queue
    trajectory_queue = Queue()

    # Create ROS node
    node = Node(trajectory_queue)
    node_thread = threading.Thread(target=node.Run)
    node_thread.start()

    # Create graphics root
    root = tk.Tk()

    # Create custom graphics application
    application = Application(root, trajectory_queue)

    # Start. Blocks until main window closes.
    root.mainloop()

    # If window closed, kill rospy
    rospy.signal_shutdown('Quit')

    # Wait for node thread
    node_thread.join()


if __name__ == "__main__":
    main()
