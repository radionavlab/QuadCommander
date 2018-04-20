
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

from line import *
from circle import *
from action_list import *
from action_config import *
from application import *

def AddCircleActionBar(application, action_list):
    application.AddActionConfigBar(
        ActionConfig()
            .Name("Circle")
            .EntryLabels(["Initial Point", "Center Point", "Period", "Arc Angle"])
            .Callback(AddCircleController(application, action_list).Handle))

def AddLineActionBar(application, action_list):
    application.AddActionConfigBar(
        ActionConfig()
            .Name("Line")
            .EntryLabels(["Start Point", "End Point", "Time"])
            .Callback(AddLineController(application, action_list).Handle))

def main():
    root = tk.Tk()
    action_list = ActionList()

    application = Application(root, action_list)
    AddCircleActionBar(application, action_list)
    AddLineActionBar(application, action_list)

    root.mainloop()


if __name__ == "__main__":
    main()
