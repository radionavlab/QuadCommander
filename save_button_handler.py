import pickle

class SaveButtonHandler:
    def __init__(self, action_list):
        self.__action_list = action_list

    def Handle(self, file_path): 
        pickle.dump(self.__action_list, open(file_path, "wb"))  
