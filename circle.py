import numpy as np

class Circle:
    def __init__(self, center_point, start_point, point_of_interest, tangential_velocity, arc_angle):
        self.__center_point         = center_point
        self.__start_point          = start_point
        self.__point_of_interest    = point_of_interest
        self.__tangential_velocity  = tangential_velocity 
        self.__arc_angle            = arc_angle

        # Configure the derived properties
        self.__cfg__()


    def __cfg__(self):
        """
        Configure derived properties. Removed from constructor for json purposes
        """
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

        yaw = np.arctan2(
                self.__point_of_interest[1] - pos[1],
                self.__point_of_interest[0] - pos[0],
                )

        vel = np.zeros(pos.shape)
        for i in xrange(pos.shape[1]):
            # velocity = tangential_velocity * normalize(cross(+z-axis, r))
            r = pos[:,i] - self.__center_point
            direction = np.cross(np.array([0, 0, 1]), r)
            vel[:,i] = self.__tangential_velocity * (direction / np.linalg.norm(direction))

        acc = np.zeros(pos.shape)
        for i in xrange(pos.shape[1]):
            # Centripetal acceleration = v * v * -r / norm(r)^2
            r = pos[:,i] - self.__center_point
            acc[:,i] = self.__tangential_velocity * self.__tangential_velocity * -r / np.power(np.linalg.norm(r), 2)

        return np.vstack((pos, yaw, vel, acc))

    def __getstate__(self):
        """
        Return the state to be serialized with json. 
        """
        state = {}
        state['_Circle__center_point']           = self.__center_point
        state['_Circle__start_point']            = self.__start_point
        state['_Circle__point_of_interest']      = self.__point_of_interest
        state['_Circle__tangential_velocity']    = self.__tangential_velocity
        state['_Circle__arc_angle']              = self.__arc_angle

        return state

    
    def __setstate__(self, state):
        """
        Fill object from unserialized json
        """
        self.__dict__.update(state)
        self.__cfg__()

