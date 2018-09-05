import numpy as np
import json

class ActionList:
    def __init__(self, actions=[]):
        self.__action_list = actions

    def Copy(self, other):
        self.__action_list = other.__action_list

    
    def AddAction(self, action):
        self.__action_list.append(action)


    def AddActions(self, actions):
        self.__action_list.extend(actions)


    def Serialize(self, frequency):
        return [action.Serialize(frequency) for action in self.__action_list]
