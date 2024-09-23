import tkinter as tk
import Section
import logging

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def inverse_colour(colour):
    rev = f"#{''.join([f'{255 - int(colour[pos:pos + 2], 16):02x}' for pos in range(1, 7, 2)])}"
    logger.debug(f"Reversing colour {colour} > {rev}")
    return rev


class Section_GUI:
    variables = {
        "Height": 0.5,  # Percent screen height that window takes up
        "Width": 0.5,  # Percent screen width that window takes up
        "Grid Colour": ["gray", "lightgray", "lightblue", "white"],  # Colours of GUI interface
        "Tile": ["#000000", "#ff0000", "#00ff00", "#0000ff"]
    }
    variables["Inverse Tile"] = [inverse_colour(col) for col in variables["Tile"]]
    grid_frame, toolbar_frame, information_frame, layer_frame = (None, None, None, None)
    GUI_feature = []
    paint = 0

    def __init__(self, section_obj):
        """
        Creates a window GUI object
        """

        logging.debug(f"Window scale (HxW): {self.variables['Height']: .2f}x{self.variables['Width']: .2f}")
        self.section_obj = section_obj
        self.create_GUI()

    def draw_grid(self, frame):
        """
        Draws the working grid within a given frame

        :param frame: Grid frame to work on
        """

        logging.debug("Creating Grid")

        # Cycle through each value in scope and create corresponding button
        for pos, val in enumerate(self.section_obj.section):
            row, col = divmod(pos, self.section_obj.section_width)
            button = tk.Button(frame, bg=self.variables["Tile"][val],
                               fg=self.variables["Inverse Tile"][val], width=5, height=2, text=val,
                               command=lambda x=pos + (self.section_obj.current_layer * self.section_obj.section_height
                                                       * self.section_obj.section_width): self.paint_tile(x))
            button.grid(row=row + 1, column=col + 1, padx=1, pady=1)

        # Grid buttons
        tk.Button(frame, text="-", bg="#FF6666", command=lambda: self.grid_adjust(height=-1)).grid(
            row=0, column=1, columnspan=self.section_obj.section_height)
        tk.Button(frame, text="+", bg="#90EE90", command=lambda: self.grid_adjust(height=1)).grid(
            row=self.section_obj.section_height + 1, column=1, columnspan=self.section_obj.section_height)
        tk.Button(frame, text="-", bg="#FF6666", command=lambda: self.grid_adjust(width=-1)).grid(
            row=1, column=0, rowspan=self.section_obj.section_width)
        tk.Button(frame, text="+", bg="#90EE90", command=lambda: self.grid_adjust(width=1)).grid(
            row=1, column=self.section_obj.section_width + 1, rowspan=self.section_obj.section_width)

        logging.debug(f"Grid Created.\nItems: {frame.winfo_children()}")

    def paint_tile(self, index):
        self.section_obj.paint_tile(index, self.paint)
        self.update_GUI()

    def grid_adjust(self, height=0, width=0):
        self.section_obj.change_scope(width=self.section_obj.section_width + width,
                                      height=self.section_obj.section_height + height)
        self.update_GUI()


    def draw_toolbar(self, frame):
            """
            Draws toolbar within a given frame

            :param frame: Toolbar frame to work on
            """

            logging.debug("Creating Toolbar")

            # Title
            label = tk.Label(frame, text="Toolbar", bg=frame.cget("bg"))
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
            label = tk.Label(frame, text="Tile Painter:", bg=frame.cget("bg"))
            label.pack(pady=5)
            listbox = tk.Listbox(frame, selectmode=tk.SINGLE, height=len(self.variables["Tile"]))
            listbox.pack()
            for index, tile in enumerate([tiles[0] for tiles in self.variables["Tile"]]):
                listbox.insert(tk.END, f"({index}) {self.section_obj.variables['Tile'][index]}")
            listbox.select_set(self.paint)
            listbox.bind("<<ListboxSelect>>", lambda event: self.change_paint(listbox.curselection()[0]))

            logging.debug(f"Toolbar Created.\nItems: {frame.winfo_children()}")

    def change_paint(self, val):
        self.paint = val
        self.update_GUI()

    def draw_information(self, frame):
        """
        Draws information within given frame

        :param frame: Information frame to work on
        """

        logging.debug("Creating Information")

        # Title
        label = tk.Label(frame, text="Information", bg=frame.cget("bg"))
        label.pack(pady=10)

        # Information
        information = ["Name: %s" % self.section_obj.section_name,
                       "Width: %d" % self.section_obj.section_width,
                       "Height: %d" % self.section_obj.section_height,
                       "Layers: %d" % self.section_obj.section_depth]
        for _, val in enumerate(information):
            label = tk.Label(frame, text=val, bg=frame.cget("bg"))
            label.pack(pady=5)

        logging.debug(f"Information Created.\nItems: {frame.winfo_children()}")

    def draw_layers(self, frame):
        """
        Draw layer navigator within given frame

        :param frame: Layer frame to work on
        """

        logging.debug("Creating Layer toolbar")

        # Title
        label = tk.Label(frame, text="Current Layer: %d" % (self.section_obj.current_layer + 1), bg=frame.cget("bg"))
        label.grid(row=0, column=1, columnspan=self.section_obj.section_depth, padx=10)

        # Layer navigator
        for depth in range(self.section_obj.section_depth):
            button = tk.Button(frame, text="Layer %d" % (depth + 1),
                               command=lambda layer=depth: self.change_layer(layer))
            button.grid(row=1, column=depth + 1, padx=5)
        tk.Button(frame, text="-", command=lambda: self.edit_layer(-1)).grid(row=1, column=0, padx=10)
        tk.Button(frame, text="+", command=lambda: self.edit_layer(1)).grid(row=1, column=self.section_obj.section_depth
                                                                                          + 2, padx=10)

        logging.debug(f"Layer toolbar created.\nItems: {frame.winfo_children()}")

    def change_layer(self, layer):
        self.section_obj.change_scope(self.section_obj.section_height, self.section_obj.section_width, layer)
        self.update_GUI()

    def edit_layer(self, amount):
        self.section_obj.edit_layers(amount)
        self.update_GUI()

    def clear_frame(self, frame):
        # Destroy widgets
        logging.debug(f"Clearing Frame {frame}")
        for widget in frame.winfo_children():
            widget.destroy()


    def update_GUI(self):
        """
        Updates the GUI
        """

        logging.critical("Updating GUI")
        for feature in self.GUI_feature:
            # Clear frame
            self.clear_frame(feature[0])
            # Rewrite frame
            logging.debug(f"Performing {feature[1]} in frame {feature[0]}")
            feature[1](feature[0])

    def create_GUI(self):
        # Create Window
        window = tk.Tk()
        window.title(
            "Section: %s" % (self.section_obj.section_name if self.section_obj.section_name != "" else "Untitled"))
        window.resizable(False, False)

        # Set screen dimensions
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()

        # Set screen pixel dimensions
        self.variables["Heightpx"], self.variables["Widthpx"] = screen_height * self.variables["Height"], \
                                                                screen_width * self.variables["Width"]

        # Set geometry
        window.geometry("%dx%d+%d+%d" % (self.variables["Widthpx"], self.variables["Heightpx"],
                                         (screen_width - self.variables["Widthpx"]) // 2,
                                         (screen_height - self.variables["Heightpx"]) // 2))

        # Configure grid row/column
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(1, weight=1)

        # [geometry width, geometry height, column, row, draw function]
        frames = [
            [0.6, 0.85, 0, 0, self.draw_grid],
            [0.25, 0.85, 2, 0, self.draw_toolbar],
            [0.25, 0.85, 1, 0, self.draw_information],
            [0.6, 0.2, 0, 1, self.draw_layers]]

        for index, item in enumerate(frames):
            frame = tk.Frame(window, width=self.variables["Widthpx"] * item[0],
                             height=self.variables["Heightpx"] * item[1], bg=self.variables["Grid Colour"][index])
            frame.grid_propagate(False)
            frame.pack_propagate(False)
            frame.grid(column=item[2], row=item[3], sticky="ns", padx=5, pady=5)
            self.GUI_feature.append((frame, item[4]))

        self.update_GUI()
        window.mainloop()


if __name__ == "__main__":
    gui = Section_GUI(Section.Section())
    """section = Section("Title",
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

                       1], 5, 5)"""
