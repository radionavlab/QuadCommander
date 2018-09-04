import jsonpickle as jp

class LoadButtonHandler:
    def __init__(self, application, action_list):
        self.__action_list = action_list
        self.__application = application

    def Handle(self, file_path): 
        with open(file_path, "r") as f:
            data = f.read()
            self.__action_list.Copy(jp.decode(data))

        self.__application.DrawPlot()
