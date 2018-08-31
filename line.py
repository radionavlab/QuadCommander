from action import Action
import numpy as np

class Line(Action):
    def __init__(self, start_point, end_point, velocity):
        super().__init__()

        self.__start_point = start_point
        self.__end_point   = end_point
        self.__velocity    = velocity
        self.__time        = np.linalg.norm(self.__start_point - self.__end_point) / self.__velocity

    def Serialize(self, frequency):
        dt = self.__time / frequency
        return np.vstack((
            np.linspace(self.__start_point[0], self.__end_point[0], dt, endpoint=True),
            np.linspace(self.__start_point[1], self.__end_point[1], dt, endpoint=True),
            np.linspace(self.__start_point[2], self.__end_point[2], dt, endpoint=True)))



