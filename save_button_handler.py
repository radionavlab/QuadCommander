import jsonpickle as jp
import subprocess

class SaveButtonHandler:
    def __init__(self, action_list):
        self.__action_list = action_list

    def Handle(self, file_path): 
        with open(file_path, "w") as f:
            print(jp.encode(self.__action_list), file=f)

        # Pretty print
        command = \
                "mv " + file_path + " " + file_path + ".tmp; " + \
                "cat " + file_path + ".tmp | python -m json.tool > " + file_path + "; " \
                "rm " + file_path + ".tmp;"
        process = subprocess.run(command, shell=True, check=True)

