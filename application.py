import tkinter as tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button

from line import Line
from circle import Circle
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
        self.__root.minsize(1500, 1000)

        # Set grid positions for top-level frames
        self.__action_config_frame.grid(row=0)
        self.__option_config_frame.grid(row=1)
        self.__plot_frame.grid(row=2)

        # Don't propogate grid properties to children
        self.__action_config_frame.grid_propagate(False)
        self.__plot_frame.grid_propagate(False)
        self.__option_config_frame.grid_propagate(False)

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

        # Add execute trajectory button
        tk.Button(self.__option_config_frame, text="Execute", command=self.AnimatePlot).pack(side="left", padx=(10,0))

        LoadButtonHandler(self, self.__action_list).Handle('archive/circle.json')



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
        subplot = figure.add_subplot(111, projection='3d')

        # Serialize the action list and display it
        data_list = self.__action_list.Serialize(0.05)
        for data in data_list:
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


    def AnimatePlot(self):
        import matplotlib.animation as animation
        import mpl_toolkits.mplot3d.axes3d as p3

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

        scat = subplot.scatter( 0, 0, 0 )

        subplot.set_xlabel("X (m)")
        subplot.set_ylabel("Y (m)")
        subplot.set_zlabel("Z (m)")

        def animate(i):
            print(i)
            offset = ( 
                    trajectory[0,i],
                    trajectory[1,i],
                    trajectory[2,i]
            )

            scat._offsets3d = (1, 2, 3)

        ani = animation.FuncAnimation(
                fig=figure, func=animate, frames=np.arange(0, num_points), interval=50, blit=False)

        # Draw
        canvas.draw()


