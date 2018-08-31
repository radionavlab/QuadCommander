import tkinter as tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button

from line import Line
from circle import Circle

import numpy as np


import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

class Application(tk.Frame):
    def __init__(self, root, action_list):
        super().__init__(root)
        self.__root                 = root
        self.__action_list          = action_list
        self.__action_config_frame  = tk.Frame(self.__root)
        self.__plot_frame           = tk.Frame(self.__root)
        self.__option_config_frame  = tk.Frame(self.__root)

        self.__configure__()


    def __configure__(self):
        # Application settings
        self.__root.title("Application")
        self.__root.minsize(800, 800)

        # Set grid positions for top-level frames
        self.__action_config_frame.grid(row=0)
        self.__plot_frame.grid(row=1)
        self.__option_config_frame.grid(row=2)

        # Don't propogate grid properties to children
        self.__action_config_frame.grid_propagate(False)
        self.__plot_frame.grid_propagate(False)
        self.__option_config_frame.grid_propagate(False)

        # Add option buttons
        tk.Button(self.__option_config_frame, text="Save", command=None).pack(side="left", padx=(10,0))
        tk.Button(self.__option_config_frame, text="Load", command=None).pack(side="left", padx=(10,0))
        tk.Button(self.__option_config_frame, text="Execute", command=None).pack(side="left", padx=(10,0))



    def AddActionConfigBar(self, action_config):
        frame = tk.Frame(self.__action_config_frame)
        action_config.Build(frame)
        frame.pack(side="top", anchor="w")
         

    def DrawPlot(self):
        # Clear any previous children
        for widget in self.__plot_frame.winfo_children():
            widget.destroy()

        figure = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(figure, master=self.__plot_frame)
        canvas.get_tk_widget().pack()
        subplot = figure.add_subplot(111, projection='3d')

        # Serialize the action list and display it
        data = self.__action_list.Serialize(0.05)
        subplot.plot(data[0,:], data[1,:], data[2,:])

        # Labels and limits
        subplot.set_xlabel("X (m)")
        subplot.set_ylabel("Y (m)")
        subplot.set_zlabel("Z (m)")

        subplot.set_xlim(-3, 3)
        subplot.set_ylim(-3, 3)
        subplot.set_zlim(0,3)

        # Draw
        canvas.draw()
