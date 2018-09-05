import numpy as np
from line import Line

class AddLineHandler:
    def __init__(self, application, action_list):
        self.__application = application
        self.__action_list = action_list

    def Handle(self, input_list): 
        start_point       = self.__parse_vector(input_list[0])
        end_point         = self.__parse_vector(input_list[1])
        point_of_interest = self.__parse_vector(input_list[2])
        velocity          = self.__parse_vector(input_list[3])

        self.__action_list.AddAction(
            Line(start_point,
                 end_point,
                 point_of_interest,
                 velocity)
        )

        self.__application.DrawPlot()


    def __parse_vector(self, string):
        return np.fromstring(string, dtype=float, sep=' ')
