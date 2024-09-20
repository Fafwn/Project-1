import logging
import math
import tkinter as tk

logger = logging.getLogger(__name__)


def inverse_colour(colour):
    return "#%s" % "".join([f'{255 - int(colour[pos:pos + 2], 16):02x}' for pos in range(1, 7, 2)])


class Section:
    """
    Provides a GUI to edit sections.

    Yet to be implemented:
        - Toolbar button functionality!!!
    """

    variables = {
        "Height": 0.5,  # Percent screen height that window takes up
        "Width": 0.5,  # Percent screen width that window takes up
        "Max Tile": 10,  # Maximum vertical and horizontal tiles
        "Max Layer": 7,  # Maximum layers
        "Grid Colour": ["gray", "lightgray", "lightblue"],  # Colours of GUI interface
        "Default Width": 5,
        "Default Height": 5,
        "Tile": [["None", "#000000"],
                 ["Walkable", "#FF0000"],
                 ["Custom1", "#00FF00"],
                 ["Custom2", "#0000FF"]]  # Different types of placeable tiles
    }
    # Initialisation
    section_name = ""
    section_height, section_width, section_depth = (0, 0, 1)
    current_layer = 0
    data, section = [], []
    grid_frame, toolbar_frame, information_frame, layer_frame = (None, None, None, None)
    paint = 0

    def __init__(self, name=None, data=None, width=variables["Default Width"], height=variables["Default Height"]):
        """
        Initialises section object

        :param name: Name of section
        :param data: The full section data. Default None
        :param width: The scope width
        :param height: The scope height
        """

        self.section_name = name  # Set name
        self.data = data if data is not None else [0 for _ in range(width * height)]  # Set data
        self.change_scope(height=height, width=width)  # Set scope
        self.create_GUI()  # Create

    def change_scope(self, height=None, width=None, layer=None):
        """
        Changes/updates the working scope

        :param height: Height of scope
        :param width: Width of scope
        :param layer: Which layer scope is on
        """

        # Set default values
        height = height or self.section_height
        width = width or self.section_width
        layer = layer if layer is not None else self.current_layer  # different bc layer can == 0

        # Bind
        height, width = (min(max(1, val), self.variables["Max Tile"]) for val in (height, width))

        # New area
        new_area = height * width

        # Update dimensions
        if height != self.section_height or width != self.section_width:
            if width > self.section_width and self.section_width:  # Width increase
                self.data = [item for sublist in
                             [self.data[pos:pos + self.section_width] + [0 for _ in range(width - self.section_width)]
                              for pos in range(0, len(self.data), self.section_width)] for item in sublist]
            elif width < self.section_width and self.section_width:  # Width decrease
                self.data = [item for sublist in [self.data[pos:pos + width] for pos in
                                                  range(0, len(self.data), self.section_width)] for item in sublist]
            elif height > self.section_height and self.section_height:  # Height increase
                self.data = [item for sublist in
                             [self.data[pos:pos + (self.section_width * self.section_height)] +
                              [0 for _ in range(self.section_width * (height - self.section_height))] for pos in
                              range(0, len(self.data), self.section_width * self.section_height)] for item in sublist]
            elif height < self.section_height and self.section_height:  # Height decrease
                self.data = [item for sublist in [self.data[pos:pos + new_area] for pos in
                                                  range(0, len(self.data), self.section_width * self.section_height)]
                             for item in sublist]

        # Update section components
        self.section_height, self.section_width, self.section_depth = height, width, max(1, math.ceil(
            len(self.data) / (height * width)))

        # Pad/Truncate
        self.data = self.data[:new_area * self.section_depth] + [0] * max(0, new_area * self.section_depth - len(
            self.data))

        # Update section
        self.section, self.current_layer = self.data[new_area * layer: new_area * (layer + 1)], layer

        if self.grid_frame is not None:  # if GUI is initialised
            self.update_GUI()

    def edit_layers(self, amount):
        """
        Edit the amount of layers

        :param amount: Can be a positive or negative number that increases layers by amount
        """

        if 1 <= self.section_depth + amount <= self.variables["Max Layer"]:  # Binds layers
            area = self.section_height * self.section_width
            if amount > 0:  # Increase layers
                self.data += [0 for _ in range(area * amount)]
            else:  # Decrease layers
                self.data = self.data[:len(self.data) + (area * amount)]

            # Update
            self.change_scope()

    def paint_tile(self, index):
        """
        "Paints" the index within self.data to the paint value

        :param index: Index of self.data to change
        """

        # Change Value
        self.data[index] = self.paint

        # Update
        self.change_scope()

    def change_paint(self, val):
        """
        Change the paint value

        :param val: value to change to
        """

        self.paint = val

    def draw_grid(self, frame):
        """
        Draws the working grid within a given frame

        :param frame: Grid frame to work on
        """

        # Destroy previous widgets
        for widget in frame.winfo_children():
            widget.destroy()

        # Cycle through each value in scope and create corresponding button
        for pos, val in enumerate(self.section):
            row, col = divmod(pos, self.section_width)
            button = tk.Button(frame, bg=self.variables["Tile"][val][1],
                               fg=inverse_colour(self.variables["Tile"][val][1]), width=5, height=2, text=val,
                               command=lambda x=pos + (self.current_layer * self.section_height * self.section_width):
                               self.paint_tile(x))
            button.grid(row=row, column=col, padx=1, pady=1)

    def draw_toolbar(self, frame):
        """
        Draws toolbar within a given frame

        :param frame: Toolbar frame to work on
        """

        # Destroy previous widgets
        for widget in frame.winfo_children():
            widget.destroy()

        # Title
        label = tk.Label(frame, text="Toolbar", bg=self.variables["Grid Colour"][1])
        label.pack(pady=10)

        # Buttons
        buttons = {"Edit Name": lambda: print("one"),
                   "Edit Tiles": lambda: print("two"),
                   "Options": lambda: print("three"),
                   "Save": lambda: print("four"),
                   "Exit": lambda: print("five")}
        for command, index in enumerate(buttons):
            button = tk.Button(frame, text=index, command=buttons[index])
            button.pack(pady=5)

        # Painter
        label = tk.Label(frame, text="Tile Painter:", bg=self.variables["Grid Colour"][1])
        label.pack(pady=5)
        listbox = tk.Listbox(frame, selectmode=tk.SINGLE, height=len(self.variables["Tile"]))
        listbox.pack()
        for index, tile in enumerate([tiles[0] for tiles in self.variables["Tile"]]):
            listbox.insert(tk.END, "(%d) %s" % (index, tile))
        listbox.select_set(self.paint)
        listbox.bind("<<ListboxSelect>>", lambda event: self.change_paint(listbox.curselection()[0]))

    def draw_information(self, frame):
        """
        Draws information within given frame

        :param frame: Information frame to work on
        """

        # Destroy previous widgets
        for widget in frame.winfo_children():
            widget.destroy()

        # Title
        label = tk.Label(frame, text="Information", bg=self.variables["Grid Colour"][2])
        label.pack(pady=10)

        #Information
        information = ["Name: %s" % self.section_name,
                       "Width: %d" % self.section_width,
                       "Height: %d" % self.section_height,
                       "Layers: %d" % self.section_depth]
        for _, val in enumerate(information):
            label = tk.Label(frame, text=val, bg=self.variables["Grid Colour"][2])
            label.pack(pady=5)

    def draw_layers(self, frame):
        """
        Draw layer navigator within given frame

        :param frame: Layer frame to work on
        """

        # Destroy previous widgets
        for widget in frame.winfo_children():
            widget.destroy()

        # Title
        label = tk.Label(frame, text="Current Layer: %d" % (self.current_layer + 1))
        label.grid(row=0, column=1, columnspan=self.section_depth, padx=10)

        # Layer navigator
        for depth in range(self.section_depth):
            button = tk.Button(frame, text="Layer %d" % (depth + 1),
                               command=lambda layer=depth: self.change_scope(self.section_height, self.section_width,
                                                                             layer))
            button.grid(row=1, column=depth + 1, padx=5)
        tk.Button(frame, text="-", command=lambda: self.edit_layers(-1)).grid(row=1, column=0, padx=10)
        tk.Button(frame, text="+", command=lambda: self.edit_layers(1)).grid(row=1, column=self.section_depth + 2,
                                                                             padx=10)

    def create_GUI(self):
        """
        Creates a window GUI object
        """

        # Set Window
        window = tk.Tk()
        window.title("Section: %s" % (self.section_name if self.section_name != "" else "Untitled"))
        window.resizable(False, False)

        # Set screen dimensions
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()

        # Set screen pixel dimensions
        self.variables["Heightpx"], self.variables["Widthpx"] = screen_height * self.variables["Height"], screen_width * \
                                                                self.variables["Width"]

        # Set geometry
        window.geometry("%dx%d+%d+%d" % (self.variables["Widthpx"], self.variables["Heightpx"],
                                         (screen_width - self.variables["Widthpx"]) // 2,
                                         (screen_height - self.variables["Heightpx"]) // 2))

        # Configure grid row/column
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(1, weight=1)

        #  Grid
        self.grid_frame = tk.Frame(window, width=self.variables["Widthpx"] / 2,
                                   height=self.variables["Heightpx"] * 0.8, bg=self.variables["Grid Colour"][0])
        self.grid_frame.grid_propagate(False)
        self.grid_frame.grid(row=1, column=1, sticky="nswe")

        # Grid buttons
        tk.Button(window, text="-", bg="#FF6666",
                  command=lambda: self.change_scope(self.section_height - 1, self.section_width,
                                                    self.current_layer)).grid(row=0, column=1)
        tk.Button(window, text="+", bg="#90EE90",
                  command=lambda: self.change_scope(self.section_height + 1, self.section_width,
                                                    self.current_layer)).grid(row=2, column=1)
        tk.Button(window, text="-", bg="#FF6666",
                  command=lambda: self.change_scope(self.section_height, self.section_width - 1,
                                                    self.current_layer)).grid(row=1, column=0)
        tk.Button(window, text="+", bg="#90EE90",
                  command=lambda: self.change_scope(self.section_height, self.section_width + 1,
                                                    self.current_layer)).grid(row=1, column=2)

        #  Toolbar
        self.toolbar_frame = tk.Frame(window, width=self.variables["Widthpx"] // 5, bg=self.variables["Grid Colour"][1])
        self.toolbar_frame.pack_propagate(False)
        self.toolbar_frame.grid(row=0, column=4, rowspan=2, sticky="ns", padx=10, pady=10)

        #  Information
        self.information_frame = tk.Frame(window, width=self.variables["Widthpx"] // 5,
                                          bg=self.variables["Grid Colour"][2])
        self.information_frame.pack_propagate(False)
        self.information_frame.grid(row=0, column=3, rowspan=2, sticky="ns", padx=10, pady=10)

        #  Layers
        self.layer_frame = tk.Frame(window)
        self.layer_frame.grid(row=3, column=0, columnspan=3, sticky="ns", padx=10)

        self.update_GUI()
        window.mainloop()

    def update_GUI(self):
        """
        Updates the GUI
        """

        self.draw_grid(self.grid_frame)
        self.draw_toolbar(self.toolbar_frame)
        self.draw_information(self.information_frame)
        self.draw_layers(self.layer_frame)


if __name__ == "__main__":
    section = Section("Title",
                      [0, 0, 1, 0, 0,
                       0, 1, 1, 1, 0,
                       1, 1, 2, 1, 1,
                       1, 2, 2, 2, 0,
                       0, 1, 1, 0, 0,

                       0, 0, 0, 0, 0,
                       0, 1, 1, 1, 0,
                       1, 2, 3, 2, 1,
                       1, 3, 3, 3, 0,
                       0, 0, 2, 0, 0,

                       1], 5, 5)
