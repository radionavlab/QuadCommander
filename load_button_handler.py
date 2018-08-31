import pickle

class LoadButtonHandler:
    def __init__(self, application, action_list):
        self.__application = application
        self.__action_list = action_list

    def Handle(self, file_path): 
      self.__action_list = pickle.load(open(file_path, "rb"))  
      print(self.__action_list)
      self.__application.DrawPlot()
