
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

from line           import *
from circle         import *
from action_list    import *
from config_bar     import *
from application    import *

def AddCircleConfigBar(application, action_list):
    application.AddActionConfigBar(
        ConfigBar()
            .Name("Circle")
            .EntryLabels(["Center Point", "Start Point", "Tangential Velocity", "Arc Angle"])
            .ButtonText("Add")
            .Callback(AddCircleHandler(application, action_list).Handle))

def AddLineConfigBar(application, action_list):
    application.AddActionConfigBar(
        ConfigBar()
            .Name("Line")
            .EntryLabels(["Start Point", "End Point", "Velocity"])
            .ButtonText("Add")
            .Callback(AddLineHandler(application, action_list).Handle))

def main():
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
