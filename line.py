import numpy as np

class Line:
    def __init__(self, start_point, end_point, point_of_interest, velocity):
        self.__start_point       = start_point
        self.__end_point         = end_point
        self.__point_of_interest = point_of_interest
        self.__velocity          = velocity

        self.__cfg__()

    def __cfg__(self):
        self.__time = np.linalg.norm(self.__start_point - self.__end_point) / self.__velocity


    def Serialize(self, frequency):
        dt = self.__time / frequency
        pos = np.vstack((
            np.linspace(self.__start_point[0], self.__end_point[0], dt, endpoint=True),
            np.linspace(self.__start_point[1], self.__end_point[1], dt, endpoint=True),
            np.linspace(self.__start_point[2], self.__end_point[2], dt, endpoint=True)))

        # Compose yaw
        yaw = np.arctan2(
                self.__point_of_interest[1] - pos[1],
                self.__point_of_interest[0] - pos[0],
                ).reshape((1, pos.shape[1]))

        # Compose velocity
        direction = self.__end_point - self.__start_point;
        vel = self.__velocity * (direction / np.linalg.norm(direction))
        vel = np.repeat(vel[:,np.newaxis], pos.shape[1], 1)

        # Line has no acceleration
        acc = np.zeros(pos.shape)

        return np.vstack((pos, yaw, vel, acc))


    def __getstate__(self):
        """
        Return the state to be serialized with json. 
        """
        state = {}
        state['_Line__start_point']       = self.__start_point
        state['_Line__end_point']         = self.__end_point
        state['_Line__point_of_interest'] = self.__point_of_interest
        state['_Line__velocity']          = self.__velocity

        return state

    
    def __setstate__(self, state):
        """
        Fill object from unserialized json
        """
        self.__dict__.update(state)
        self.__cfg__()

