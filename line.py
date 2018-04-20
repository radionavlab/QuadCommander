from action import Action
import numpy as np

class Line(Action):
    def __init__(self, start_point, end_point, time):
        super().__init__()

        self.__start_point = start_point
        self.__end_point = end_point
        self.__time = time 

    def Serialize(self, frequency):
        dt = self.__time / frequency
        return np.vstack((
            np.linspace(self.__start_point[0], self.__end_point[0], dt, endpoint=True),
            np.linspace(self.__start_point[1], self.__end_point[1], dt, endpoint=True),
            np.linspace(self.__start_point[2], self.__end_point[2], dt, endpoint=True)))



class LineBuilder:
    def StartPoint(self, start_point):
        self.__start_point = start_point
        return self

    def EndPoint(self, end_point):
        self.__end_point = end_point
        return self

    def Time(self, time):
        self.__time = time
        return self

    def Build(self):
        return Line(self.__start_point, self.__end_point, self.__time)


class AddLineController:
    def __init__(self, application, action_list):
        self.__application = application
        self.__action_list = action_list

    def Handle(self, input_list):
        # Inputs are:
        # 1) Start point -> numpy 3 vector
        # 2) End point -> numpy 3 vector
        # 3) Time -> real, positive scalar
        
        start_point = self.__parse_vector(input_list[0])
        end_point   = self.__parse_vector(input_list[1])
        time        = self.__parse_vector(input_list[2])

        self.__action_list.AddAction(
            LineBuilder()
                .StartPoint(start_point)
                .EndPoint(end_point)
                .Time(time)
                .Build())

        self.__application.DrawPlot()


    def __parse_vector(self, string):
        return np.fromstring(string, dtype=float, sep=',')
