import tkinter as tk
import Section
from Code.Imports.ConfigMaster import Config
import logging

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

def inverse_colour(colour):
    rev = f"#{''.join([f'{255 - int(colour[pos:pos + 2], 16):02x}' for pos in range(1, 7, 2)])}"
    logger.debug(f"Reversing colour {colour} > {rev}")
    return rev


class Section_GUI:
    """
    Object that handles the graphical user interface for a section object
    Please replace this file with a better GUI eventually
    """

    variables = Config("Interactive").data
    variables["Inverse Tile"] = [inverse_colour(col) for col in variables["Tile Colour"]]
    GUI_feature = []
    paint = 0

    def __init__(self, section_obj):
        """
        Initialises a window GUI object with given section object

        :param section_obj: Section.Section: The section object to work with
        :return: None
        """

        logging.debug(f"Window scale (HxW): "
                      f"{self.variables['Height Percentage']: .2f}x{self.variables['Width Percentage']: .2f}")
        self.section_obj = section_obj
        self.create()

    def draw_grid(self, frame):
        """
        Draws the working grid within a given frame

        :param frame: tk.Frame: Grid frame to work on
        """

        logging.debug("Creating Grid")

        # Cycle through each value in scope and create corresponding button
        for pos, val in enumerate(self.section_obj.section):
            row, col = divmod(pos, self.section_obj.section_width)
            button = tk.Button(frame, bg=self.variables["Tile Colour"][val],
                               fg=self.variables["Inverse Tile"][val], width=5, height=2, text=val, # Make this variable size
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
        """
        Paints a tile at a specific index in the section object with the currently selected paint.

        :param index: int: The index of the tile to be painted
        :return:
        """

        self.section_obj.paint_tile(index, self.paint)
        self.update()

    def grid_adjust(self, height=0, width=0):
        """
        Adjusts the grid size of the section object by the provided amount.

        :param height: int: The amount by which to adjust the height
        :param width: int: The amount by which to adjust the width
        :return: None
        """

        self.section_obj.change_scope(width=self.section_obj.section_width + width,
                                      height=self.section_obj.section_height + height)
        self.update()


    def draw_toolbar(self, frame):
        """
        Draws toolbar within a given frame. Toolbar includes buttons for editing, options, saving, exiting, and
        changing tile painter.

        :param frame: tk.Frame: Toolbar frame to work on
        :return: None
        """

        logging.debug("Creating Toolbar")

        # Title
        label = tk.Label(frame, text="Toolbar", bg=frame.cget("bg"))
        label.pack(pady=10)

        # Buttons
        buttons = {"Edit Name": lambda: print(self.section_obj.data),
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
        listbox = tk.Listbox(frame, selectmode=tk.SINGLE, height=len(self.variables["Tile Colour"]))
        listbox.pack()
        for index, tile in enumerate(self.variables["Tile Type"]):
            listbox.insert(tk.END, f"({index}) {tile}")
        listbox.select_set(self.paint)
        listbox.bind("<<ListboxSelect>>", lambda event: self.change_paint(listbox.curselection()[0]))

        logging.debug(f"Toolbar Created.\nItems: {frame.winfo_children()}")

    def change_paint(self, val):
        """
        Changes the current paint value

        :param val: int: the new paint value to be set
        :return: None
        """

        self.paint = val
        self.update()

    def draw_information(self, frame):
        """
        Draws information within given frame

        :param frame: tk.Frame: Information frame to work on
        :return: None
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

        :param frame: tk.Frame: Layer frame to work on
        :return: None
        """

        logging.debug("Creating Layer toolbar")

        # Title
        label = tk.Label(frame, text="Current Layer: %d" % (self.section_obj.current_layer + 1), bg=frame.cget("bg"))
        label.grid(row=0, column=1, columnspan=self.section_obj.section_depth, padx=10, sticky="ns")

        # Layer navigator
        for depth in range(self.section_obj.section_depth):
            button = tk.Button(frame, text="Layer %d" % (depth + 1),
                               command=lambda layer=depth: self.change_layer(layer))
            button.grid(row=1, column=depth + 1, padx=5, sticky="ns")
        tk.Button(frame, text="-", command=lambda: self.edit_layer(-1)).grid(row=1, column=0, padx=10)
        tk.Button(frame, text="+", command=lambda: self.edit_layer(1)).grid(row=1, column=self.section_obj.section_depth
                                                                                          + 2, padx=10)

        logging.debug(f"Layer toolbar created.\nItems: {frame.winfo_children()}")

    def change_layer(self, layer):
        """
        Changes the current layer of section object

        :param layer: int: the new layer value to be set
        :return: None
        """

        self.section_obj.change_scope(self.section_obj.section_height, self.section_obj.section_width, layer)
        self.update()

    def edit_layer(self, amount):
        """
        Edits the current layer of section object by the provided amount

        :param amount: int: the amount by which to adjust the layer
        :return: None
        """

        self.section_obj.edit_layers(amount)
        self.update()


    @staticmethod
    def clear_frame(frame):
        """
        Clears all widgets from a given frame

        :param frame: tk.Frame: Frame to clear
        :return: None
        """

        logging.debug(f"Clearing Frame {frame}")
        for widget in frame.winfo_children():
            widget.destroy()


    def update(self):
        """
        Updates the GUI by clearing and redrawing all widgets in the GUI

        :param: :return: None
        """

        logging.debug("Updating GUI")
        for feature in self.GUI_feature:
            # Clear frame
            self.clear_frame(feature[0])
            # Rewrite frame
            logging.debug(f"Performing {feature[1]} in frame {feature[0]}")
            feature[1](feature[0])

    def create(self):
        """
        Creates and configures the main window for the GUI

        :param: :return: None
        """

        # Create Window
        window = tk.Tk()
        window.title(
            "Section: %s" % (self.section_obj.section_name if self.section_obj.section_name != "" else "Untitled"))
        window.resizable(False, False)

        # Set screen dimensions
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()

        # Set screen pixel dimensions
        self.variables["Heightpx"], self.variables["Widthpx"] = screen_height * self.variables["Height Percentage"], \
                                                                screen_width * self.variables["Width Percentage"]

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

        self.update()
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
