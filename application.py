import tkinter as tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button

from line import Line
from circle import Circle
from action_list import ActionList
from config_bar import ConfigBar
from add_circle_handler import AddCircleHandler
from add_line_handler import AddLineHandler
from popup_text_box import PopupTextBox
from save_button_handler import SaveButtonHandler
from load_button_handler import LoadButtonHandler

import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

class Application(tk.Frame, object):
    def __init__(self, root, trajectory_queue):
        super(Application, self).__init__(root)
        self.__root                 = root
        self.__trajectory_queue     = trajectory_queue
        self.__action_config_frame  = tk.Frame(self.__root)
        self.__plot_frame           = tk.Frame(self.__root)
        self.__option_config_frame  = tk.Frame(self.__root)

        self.__action_list = ActionList()

        self.__configure__()


    def __configure__(self):
        # Application settings
        self.__root.title("Application")
        self.__root.minsize(1500, 1000)

        # Set grid positions for top-level frames
        self.__action_config_frame.grid(row=0)
        self.__option_config_frame.grid(row=1)
        self.__plot_frame.grid(row=2)

        # Don't propogate grid properties to children
        self.__action_config_frame.grid_propagate(False)
        self.__plot_frame.grid_propagate(False)
        self.__option_config_frame.grid_propagate(False)

        # Add circle config bar
        self.AddActionConfigBar(
            ConfigBar()
                .Name("Circle")
                .EntryLabels(["Center Point", "Start Point", "Point of Interest", "Tangential Velocity", "Arc Angle"])
                .ButtonText("Add")
                .Callback(AddCircleHandler(self, self.__action_list).Handle))
    
        # Add line config bar
        self.AddActionConfigBar(
            ConfigBar()
                .Name("Line")
                .EntryLabels(["Start Point", "End Point", "Point of Interest", "Velocity"])
                .ButtonText("Add")
                .Callback(AddLineHandler(self, self.__action_list).Handle))

        # Add save button
        tk.Button(self.__option_config_frame, text="Save",
                command=PopupTextBox(
                    window_title="Save",
                    button_text="Save",
                    label_text="Save Path",
                    button_command=SaveButtonHandler(self.__action_list).Handle).Popup
                ).pack(side="left", padx=(10,0))

        # Add load button
        tk.Button(self.__option_config_frame, text="Load",
                command=PopupTextBox(
                    window_title="Load",
                    button_text="Load",
                    label_text="Load Path",
                    button_command=LoadButtonHandler(self, self.__action_list).Handle).Popup
                ).pack(side="left", padx=(10,0))

        # Add preview button
        tk.Button(self.__option_config_frame, text="Preview", command=self.AnimatePlot).pack(side="left", padx=(10,0))

        # Add execute trajectory button
        tk.Button(self.__option_config_frame, text="Execute", command=
                lambda: self.__trajectory_queue.put(np.concatenate(self.__action_list.Serialize(0.05), 1))
                ).pack(side="left", padx=(10,0))

        LoadButtonHandler(self, self.__action_list).Handle('/home/tuckerhaydon/ROS/src/QuadCommander/archive/circle.json')
        # LoadButtonHandler(self, self.__action_list).Handle('archive/rectangle.json')


    def AddActionConfigBar(self, action_config):
        frame = tk.Frame(self.__action_config_frame)
        action_config.Build(frame)
        frame.pack(side="top", anchor="w")
         

    def DrawPlot(self):
        # Clear any previous children
        for widget in self.__plot_frame.winfo_children():
            widget.destroy()

        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=self.__plot_frame)
        canvas.get_tk_widget().pack()
        subplot = p3.Axes3D(figure)

        # Serialize the action list and display it
        data_list = self.__action_list.Serialize(0.05)
        for data in data_list:

            # Plot the trajectory
            subplot.plot(data[0,:], data[1,:], data[2,:])
    
            # Plot the yaw
            subplot.quiver(
                    data[0,::20],
                    data[1,::20],
                    data[2,::20],
                    np.cos(data[3,::20]),
                    np.sin(data[3,::20]),
                    0,
                    length=0.5, 
                    pivot='tail'
            )

        # Labels and limits
        subplot.set_xlabel("X (m)")
        subplot.set_ylabel("Y (m)")
        subplot.set_zlabel("Z (m)")

        subplot.set_xlim(-3, 3)
        subplot.set_ylim(-3, 3)
        subplot.set_zlim(0,3)

        # Draw
        canvas.draw()


    def AnimatePlot(self):
        for widget in self.__plot_frame.winfo_children():
            widget.destroy()

        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=self.__plot_frame)
        canvas.get_tk_widget().pack()
        subplot = p3.Axes3D(figure)

        # Serialize the action list and display it
        paths = self.__action_list.Serialize(0.05)
        for path in paths:
            subplot.plot(path[0,:], path[1,:], path[2,:])

        trajectory = np.concatenate([path for path in paths], 1)
        num_points = trajectory.shape[1]

        scat = subplot.scatter(
            xs=np.array([0]),
            ys=np.array([0]),
            zs=np.array([0]),
            s=200,
            marker="*",
            c='k'
            )

        quiv = subplot.quiver(
                np.array([0]),
                np.array([0]),
                np.array([0]),
                np.array([0]),
                np.array([0]),
                np.array([0]),
                length=0.1
                )

        subplot.set_xlabel("X (m)")
        subplot.set_ylabel("Y (m)")
        subplot.set_zlabel("Z (m)")

        def animate(i):
            scat._offsets3d = (
                    np.array([trajectory[0,i]]),
                    np.array([trajectory[1,i]]),
                    np.array([trajectory[2,i]])
                    )

            quiv.set_segments([[
                [
                    trajectory[0,i],
                    trajectory[1,i],
                    trajectory[2,i]
                ],
                [
                    trajectory[0,i] + np.cos(trajectory[3,i]),
                    trajectory[1,i] + np.sin(trajectory[3,i]),
                    trajectory[2,i]
                ],
                ]])

        ani = animation.FuncAnimation(
                fig=figure, func=animate, frames=np.arange(0, num_points), interval=50, blit=False, repeat=False)

        # Draw
        canvas.draw()


