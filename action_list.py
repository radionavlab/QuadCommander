import numpy as np
from action import Action


class ActionList(Action):

    def __init__(self, actions=[]):
        self.__action_list = actions

    def Copy(self, other):
        self.__action_list = other.__action_list

    
    def AddAction(self, action):
        self.__action_list.append(action)


    def AddActions(self, actions):
        self.__action_list.extend(actions)


    def Serialize(self, frequency):
        return np.concatenate([action.Serialize(frequency) for action in self.__action_list], 1) 

