from action import Action
import numpy as np

class Circle(Action):
    def __init__(self, initial_point, center_point, time, arc_angle=2*np.pi):
        """
        initial_point       - numpy 3-vector
        center_point        - numpy 3 vector
        time                - time in seconds to complete arc
        arc_angle           - angle in radians for circle path. Counter clockwise = positive
        """
        super().__init__()

        self.__initial_point        = initial_point
        self.__time                 = time
        self.__arc_angle            = arc_angle
        self.__center_point         = center_point

        self.__radius               = np.linalg.norm(self.__initial_point - self.__center_point)
        self.__initial_angle        = np.arctan2(
                                        (self.__initial_point - self.__center_point)[1], 
                                        (self.__initial_point - self.__center_point)[0])
        self.__angular_velocity     = self.__arc_angle / self.__time
        self.__tangential_velocity  = self.__arc_angle * self.__radius / self.__time


    def Serialize(self, frequency): 
        dtheta = np.linspace(0, self.__arc_angle, self.__time / frequency, endpoint=True)
        theta = np.mod(self.__initial_angle + dtheta, 2*np.pi)

        dr = self.__radius * np.array([np.cos(theta), np.sin(theta), np.zeros(theta.shape)])
        pos = dr + np.reshape(self.__center_point, (dr.shape[0],1))

        return pos 



class CircleBuilder:
    def CenterPoint(self, center_point):
        """ numpy 3 vector: Center point of circle """
        self.__center_point = center_point
        return self

    def RadialVector(self, radial_vector):
        """ numpy 3 vector: Vector from center to initial point """
        self.__radial_vector = radial_vector
        return self

    def InitialPoint(self, initial_point):
        """ numpy 3 vector: Initial point along edge of circle """
        self.__initial_point = initial_point
        return self

    def ArcAngle(self, arc_angle):
        """ real scalar: Angle in radians of an arc """
        self.__arc_angle = arc_angle
        return self

    def Time(self, time):
        """ real scalar: Time to complete the arc """
        self.__time = time
        return self

    def AngularVelocity(self, angular_velocity):
        """ real scalar: Angular velocity to complete the arc with """
        self.__angular_velocity = angular_velocity
        return self

    def TangentialVelocity(self, tangential_velocity):
        """ real scalar: Tangential velocity to complete arc with """
        self.__tangential_velocity = tangential_velocity
        return self

    def Build(self):
        return Circle(self.__initial_point, self.__center_point, self.__time, self.__arc_angle)




class AddCircleController:

    def __init__(self, application, action_list):
        self.__application = application
        self.__action_list = action_list

    def Handle(self, input_list):

        # Inputs are: 
        # 1) Initial point -> numpy 3 vector
        # 2) Center point  -> numpy 3 vector
        # 3) Time          -> real, positive scalar
        # 4) Arc Angle     -> real scalar

        initial_point = self.__parse_vector(input_list[0])
        center_point  = self.__parse_vector(input_list[1])
        time          = self.__parse_vector(input_list[2])
        arc_angle     = self.__parse_vector(input_list[3])

        self.__action_list.AddAction(
            CircleBuilder()
                .InitialPoint(initial_point)
                .CenterPoint(center_point)
                .Time(time)
                .ArcAngle(arc_angle)
                .Build())

        self.__application.DrawPlot()

    def __parse_vector(self, string):
        return np.fromstring(string, dtype=float, sep=',')
