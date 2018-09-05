#!/usr/bin/python2

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
import jsonpickle.ext.numpy as jp_numpy

from line                   import Line
from circle                 import Circle
from action_list            import ActionList
from config_bar             import ConfigBar
from application            import Application
from add_circle_handler     import AddCircleHandler
from add_line_handler       import AddLineHandler

def AddCircleConfigBar(application, action_list):
    application.AddActionConfigBar(
        ConfigBar()
            .Name("Circle")
            .EntryLabels(["Center Point", "Start Point", "Point of Interest", "Tangential Velocity", "Arc Angle"])
            .ButtonText("Add")
            .Callback(AddCircleHandler(application, action_list).Handle))

def AddLineConfigBar(application, action_list):
    application.AddActionConfigBar(
        ConfigBar()
            .Name("Line")
            .EntryLabels(["Start Point", "End Point", "Point of Interest", "Velocity"])
            .ButtonText("Add")
            .Callback(AddLineHandler(application, action_list).Handle))

def main():
    # Configure the json numpy handlers
    jp_numpy.register_handlers()

    # Create graphics root
    root = tk.Tk()

    # Create action list
    action_list = ActionList()

    # Create custom graphics application
    application = Application(root, action_list)

    # Add action elements
    AddCircleConfigBar(application, action_list)
    AddLineConfigBar(application, action_list)

    # Start
    root.mainloop()


if __name__ == "__main__":
    main()
