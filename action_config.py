import tkinter as tk

class ActionConfig:
    
    def __init__(self):
        self.__entry_labels = []
        self.__string_vars = []

    def Name(self, name):
        self.__name = name
        return self

    def Callback(self, callback):
        self.__callback = callback
        return self

    def EntryLabels(self, entry_labels):
        self.__entry_labels.extend(entry_labels)
        return self

    def EntryLabel(self, entry_label):
        self.__entry_labels.append(entry_label)
        return self

    def __parse__(self):
        self.__callback([v.get() for v in self.__string_vars])
        

    def Build(self, frame):
        # Name
        tk.Label(frame, text=self.__name, font=("Helvetica", 16)).pack(padx=5, pady=10, side="left")

        # Text boxes
        counter = 0
        for label in self.__entry_labels:
            # Reference to grab input
            v = tk.StringVar()
            self.__string_vars.append(v)

            tk.Label(frame, text=label).pack(padx=(10, 0), pady=10, side="left")
            tk.Entry(frame, width=5, textvariable=v).pack(pady=10, side="left")

            counter = counter + 2

        # Add button
        tk.Button(frame, text="Add", command=self.__parse__).pack(side="left", padx=(10,0))

