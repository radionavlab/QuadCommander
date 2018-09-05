import numpy as np
from circle import Circle

class AddCircleHandler:

    def __init__(self, application, action_list):
        self.__application = application
        self.__action_list = action_list

    def Handle(self, input_list):
        center_point        = self.__parse_vector(input_list[0])
        initial_point       = self.__parse_vector(input_list[1])
        point_of_interest   = self.__parse_vector(input_list[2])
        tangential_velocity = self.__parse_vector(input_list[3])
        arc_angle           = self.__parse_vector(input_list[4])

        self.__action_list.AddAction(
            Circle(center_point,
                   initial_point,
                   point_of_interest,
                   tangential_velocity,
                   arc_angle) 
        )

        self.__application.DrawPlot()

    def __parse_vector(self, string):
        return np.fromstring(string, dtype=float, sep=' ')
