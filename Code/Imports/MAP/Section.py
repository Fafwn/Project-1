import logging
import math
from Config import Config


class Section:
    """
    Provides a GUI to edit sections.

    Yet to be implemented:
        - Toolbar button functionality!!!
    """

    variables = Config("Section").data

    # Initialisation
    section_name = ""
    section_height, section_width, section_depth = (0, 0, 1)
    current_layer = 0
    data, section = [], []

    def __init__(self, name=None, data=None, width=variables["Default Width"], height=variables["Default Height"]):
        """
        Initialises section object

        :param name: str: Name of section
        :param data: [int]: The full section data. Default None
        :param width: int: The scope width
        :param height: int: The scope height
        """

        self.section_name = name  # Set name
        self.data = data if data is not None else [0 for _ in range(width * height)]  # Set data
        self.change_scope(height=height, width=width)  # Set scope

    def change_scope(self, height=None, width=None, layer=None):
        """
        Changes/updates the working scope

        :param height: int: Height of scope
        :param width: int: Width of scope
        :param layer: int:  Which layer scope is on
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
                logging.info(f"Increasing width by {width - self.section_width} ({self.section_width}>{width})")
                self.data = [item for sublist in
                             [self.data[pos:pos + self.section_width] + [0 for _ in range(width - self.section_width)]
                              for pos in range(0, len(self.data), self.section_width)] for item in sublist]
            elif width < self.section_width and self.section_width:  # Width decrease
                logging.info(f"Decreasing width by {self.section_width - width} ({self.section_width}>{width})")
                self.data = [item for sublist in [self.data[pos:pos + width] for pos in
                                                  range(0, len(self.data), self.section_width)] for item in sublist]
            elif height > self.section_height and self.section_height:  # Height increase
                logging.info(f"Increasing height by {height - self.section_height} ({self.section_height}>{height})")
                self.data = [item for sublist in
                             [self.data[pos:pos + (self.section_width * self.section_height)] +
                              [0 for _ in range(self.section_width * (height - self.section_height))] for pos in
                              range(0, len(self.data), self.section_width * self.section_height)] for item in sublist]
            elif height < self.section_height and self.section_height:  # Height decrease
                logging.info(f"Decreasing height by {self.section_height - height} ({self.section_height}>{height})")
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

    def edit_layers(self, amount):
        """
        Edit the amount of layers

        :param amount: int: Can be a positive or negative number that increases layers by amount
        """

        if 1 <= self.section_depth + amount <= self.variables["Max Layer"]:  # Binds layers
            logging.info(
                f"{'Increasing' if amount > 0 else 'Decreasing'} layers by {abs(amount)} ({self.section_depth}>{self.section_depth + amount})")
            area = self.section_height * self.section_width
            if amount > 0:  # Increase layers
                self.data += [0 for _ in range(area * amount)]
            else:  # Decrease layers
                self.data = self.data[:len(self.data) + (area * amount)]

            # Update
            self.change_scope()

    def paint_tile(self, index, val):
        """
        "Paints" the index within self.data to the paint value

        :param index: int: Index of self.data to change
        :param val: int: Value to change into
        """

        logging.info(f"Changing index {index} to {val} ({self.data[index]}>{val})")
        # Change Value
        self.data[index] = val
        # Update
        self.change_scope()
