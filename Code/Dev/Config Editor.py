import tkinter as tk
import yaml
import os

config_name = "config.yaml"
directory = "C:/Users/kaiki/IdeaProjects/Project-1/Code/Imports"


class ConfigManager:
    default_flags = {
        "Type" : None,
        "List?" : False
    }

    def __init__(self, directory):
        self.directory = directory
        self.data = {}
        self.files = []

        self.find_config_files()
        self.select_YAML_window()

    def find_config_files(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file == config_name:
                    self.files.append(os.path.join(root, file))


    def select_YAML_window(self):
        window = tk.Tk()
        window.title("Config Editor")
        window.geometry("400x300+100+100")
        window.resizable(False,False)

        canvas = tk.Canvas(window)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0,0), window=frame, anchor="nw")

        for file_path in self.files:
            # Use the file name as button text, or full path if desired
            button = tk.Button(frame, text=file_path[len(directory)+1:], anchor="w", command=lambda p=file_path: self.configEditor(p))
            button.pack(fill="x", padx=5, pady=2)

        window.mainloop()

    def configEditor(self, address):
        self.formatData(self.load_YAML(address))


    def formatData(self, data):
        self.data = {}
        for index in list(data):
            self.data[index] = [self.identify([item, data[index][item]]) for item in data[index]]

    def identify(self, data):
        flags = self.default_flags.copy()

        name = data[0]
        content = data[1]
        if isinstance(content, list):
            flags["List?"] = True
            flags["Type"] = type(content[0])
            return [name] + content + [flags]

        else:
            flags["List?"] = False
            flags["Type"] = type(content)
            return [name] + [content] + [flags]

        #print([x for x in [[index, list(data[index])] for index in list(data)]])

    def load_YAML(self, YAML_file):
        with open(YAML_file, "r") as file:
            return yaml.safe_load(file)

if __name__ == "__main__":
    ConfigManager(directory)