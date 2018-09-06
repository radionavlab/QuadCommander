import Tkinter as tk

class PopupTextBox:
    def __init__(self, 
                 window_title="default_window_title",
                 label_text="default_label_text", 
                 button_text="default_button_text",
                 button_command=None):
        self.__window_title = window_title
        self.__label_text = label_text
        self.__button_text = button_text
        self.__button_command = button_command

    def Popup(self):
        self.__frame = tk.Tk()
        self.__frame.wm_title(self.__window_title)
        self.__label = tk.Label(self.__frame, text=self.__label_text)
        self.__button = tk.Button(self.__frame, 
                                  text=self.__button_text,
                                  command=self.__parse)
        self.__entry = tk.Entry(self.__frame)

        self.__label.pack(side="left", padx=(10,0))
        self.__entry.pack(side="left", padx=(10,0))
        self.__button.pack(side="left", padx=(10,0))

    def __parse(self):
        self.__button_command(self.__entry.get())
        self.__frame.destroy()

        
