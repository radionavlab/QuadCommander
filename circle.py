from action import Action
import numpy as np

class Circle(Action):
    def __init__(self, center_point, start_point, tangential_velocity, arc_angle):
        super().__init__()

        self.__center_point         = center_point
        self.__start_point          = start_point
        self.__tangential_velocity  = tangential_velocity 
        self.__arc_angle            = arc_angle

        self.__radius               = np.linalg.norm(self.__start_point - self.__center_point)
        self.__initial_angle        = np.arctan2(
                                        (self.__start_point - self.__center_point)[1], 
                                        (self.__start_point - self.__center_point)[0])
        self.__time                 = self.__radius * self.__arc_angle / self.__tangential_velocity
        self.__angular_velocity     = self.__arc_angle / self.__time


    def Serialize(self, frequency): 
        dtheta = np.linspace(0, self.__arc_angle, self.__time / frequency, endpoint=True)
        theta = np.mod(self.__initial_angle + dtheta, 2*np.pi)

        dr = self.__radius * np.array([np.cos(theta), np.sin(theta), np.zeros(theta.shape)])
        pos = dr + np.reshape(self.__center_point, (dr.shape[0],1))

        return pos 
