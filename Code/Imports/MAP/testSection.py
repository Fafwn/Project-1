import unittest
import Section
import random
import string


class SectionTestCase(unittest.TestCase):
    def test_section_generation_basic(self):
        default = {
            "Name": "Test section",
            "Width": random.randint(3,7),
            "Height": random.randint(3,7),
            "Depth": 1,
            "Current Layer": 0,
        }

        # Generating random data
        default["Data"] = [random.randint(0,2) for _ in range((default["Width"]*default["Height"]))]
        test_section = Section.Section(name=default["Name"], data=default["Data"], width=default["Width"], height=default["Height"])

        # Testing Name
        self.assertEqual(test_section.section_name, default["Name"], msg="Section name not as expected.")

        # Testing Data Length
        self.assertEqual(len(test_section.data), len(default["Data"]), msg="Section data length not as expected.")

        # Testing Data Values
        for i in range(len(default["Data"])):
            self.assertEqual(test_section.data[i], default["Data"][i], msg="Section data value not as expected at index {}.".format(i))

        # Testing Height
        self.assertEqual(test_section.section_height, default["Height"], msg="Section height not as expected.")

        # Testing Width
        self.assertEqual(test_section.section_width, default["Width"], msg="Section width not as expected.")

        # Testing Depth
        self.assertEqual(test_section.section_depth, default["Depth"], msg="Section depth not as expected.")

        # Testing Current Layer
        self.assertEqual(test_section.current_layer, default["Current Layer"], msg="Section current layer not as expected.")

    def test_section_generation_advanced(self):
        letters = string.ascii_lowercase + string.digits
        default = {
            "Name": "".join([random.choice(letters).upper() if random.randint(0,1) == 1 else random.choice(letters) for _ in range(random.randint(1, 25))]),
            "Width": 7,
            "Height": 8,
            "Depth": random.randint(3,5),
            "Current Layer": 0,
            "Max Tile Type": 2
        }

        # Cutting down section by random amount
        default["Data"] = [random.randint(0,default["Max Tile Type"]) for _ in range((default["Width"]*default["Height"]*default["Depth"]) - (random.randint(0, default["Width"]*default["Height"] - 1)))]
        test_section = Section.Section(name=default["Name"], data=default["Data"], width=default["Width"], height=default["Height"])

        # Testing Name
        self.assertEqual(test_section.section_name, default["Name"], msg="Section name not as expected.")

        # Testing Data length
        self.assertEqual(len(test_section.data), default["Height"]*default["Width"]*default["Depth"], msg="Section data length not as expected.")

        # Testing Data values
        for i in range(len(default["Data"])):
            self.assertEqual(test_section.data[i], default["Data"][i], msg="Section data value not as expected at index {}.".format(i))

        # Testing Height
        self.assertEqual(test_section.section_height, default["Height"], msg="Section height not as expected.")

        # Testing Width
        self.assertEqual(test_section.section_width, default["Width"], msg="Section width not as expected.")

        # Testing Depth
        self.assertEqual(test_section.section_depth, default["Depth"], msg="Section depth not as expected.")

        # Testing Current Layer
        self.assertEqual(test_section.current_layer, default["Current Layer"], msg="Section current layer not as expected.")

        # Changing Current Layer
        test_section.change_scope(layer=2)
        self.assertEqual(test_section.current_layer, 2, msg="Section current layer not changed correctly.")

    def test_section_generation_aggressive(self):
        pass

    def test_section_generation_default(self):
        default = {
            "Width": 5,
            "Height": 5,
            "Name": None
        }

        test_section = Section.Section()

        # Testing Name
        self.assertEqual(test_section.section_name, default["Name"], msg="Section name not as expected.")

        # Testing Data length
        self.assertEqual(len(test_section.data), default["Height"]*default["Width"], msg="Section data length not as expected.")

        # Testing Data values
        for i in range(len(test_section.data)):
            self.assertEqual(test_section.data[i], 0, msg="Section data value not as expected at index {}.".format(i))

        # Testing Height
        self.assertEqual(test_section.section_height, default["Height"], msg="Section height not as expected.")

        # Testing Width
        self.assertEqual(test_section.section_width, default["Width"], msg="Section width not as expected.")

        # Testing Depth
        self.assertEqual(test_section.section_depth, 1, msg="Section depth not as expected.")

        # Testing Current Layer
        self.assertEqual(test_section.current_layer, 0, msg="Section current layer not as expected.")

    def test_section_generation_failure(self):
        pass

    def test_section_edit(self):
        default = {
            "Width": 3,
            "Height": 3,
            "Data": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            "Data+W": [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0],
            "Data+H": [1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
            "Data-W": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            "Data-H": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            "Data+W2": [1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0],
            "Data+H2": [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
            "Data-W2": [1,1,1,1,1,1,1,1,1],
            "Data-H2": [1,1,1,1,1,1,1,1,1]
        }

        test_section = Section.Section(width=default["Width"], height=default["Height"], data=default["Data"])

        # Test adding width
        test_section.change_scope(width=default["Width"] + 1, height=default["Height"])
        self.assertEqual(test_section.data, default["Data+W"], msg="Section data not as expected after adding width.")
        test_section.change_scope(width=default["Width"], height=default["Height"])
        test_section.change_scope(width=default["Width"] + 2, height=default["Height"])
        self.assertEqual(test_section.data, default["Data+W2"], msg="Section data not as expected after adding width.")
        test_section.change_scope(width=default["Width"], height=default["Height"])


        # Test adding height
        test_section.change_scope(width=default["Width"], height=default["Height"] + 1)
        self.assertEqual(test_section.data, default["Data+H"], msg="Section data not as expected after adding height.")
        test_section.change_scope(width=default["Width"], height=default["Height"])
        test_section.change_scope(width=default["Width"], height=default["Height"] + 2)
        self.assertEqual(test_section.data, default["Data+H2"], msg="Section data not as expected after adding height.")
        test_section.change_scope(width=default["Width"], height=default["Height"])

        # Test subtracting width
        test_section.change_scope(width=default["Width"] - 1, height=default["Height"])
        self.assertEqual(test_section.data, default["Data-W"], msg="Section data not as expected after subtracting width.")
        test_section = Section.Section(width=default["Width"], height=default["Height"], data=default["Data"])
        test_section.change_scope(width=default["Width"] - 2, height=default["Height"])
        self.assertEqual(test_section.data, default["Data-W2"], msg="Section data not as expected after subtracting width.")
        test_section = Section.Section(width=default["Width"], height=default["Height"], data=default["Data"])

        # Test subtracting height
        test_section.change_scope(width=default["Width"], height=default["Height"] - 1)
        self.assertEqual(test_section.data, default["Data-H"], msg="Section data not as expected after subtracting height.")
        test_section = Section.Section(width=default["Width"], height=default["Height"], data=default["Data"])
        test_section.change_scope(width=default["Width"], height=default["Height"] - 2)
        self.assertEqual(test_section.data, default["Data-H2"], msg="Section data not as expected after subtracting height.")


    def test_section_layer_edit(self):
        default = {
            "Height": 4,
            "Width" : 3
        }
        test_section = Section.Section(height=default["Height"], width=default["Width"])

        self.assertEqual(len(test_section.data), default["Height"]*default["Width"], msg="Section data length not as expected.")
        test_section.edit_layers(2)
        self.assertEqual(len(test_section.data), default["Height"]*default["Width"]*3, msg="Section data length not as expected.")
        test_section.edit_layers(-1)
        self.assertEqual(len(test_section.data), default["Height"]*default["Width"]*2, msg="Section data length not as expected.")
        test_section.edit_layers(1)
        self.assertEqual(len(test_section.data), default["Height"]*default["Width"]*3, msg="Section data length not as expected.")
        test_section.edit_layers(-2)
        self.assertEqual(len(test_section.data), default["Height"]*default["Width"], msg="Section data length not as expected.")

    def test_section_paint(self):
        test_section = Section.Section(height=3, width=3)
        test_section.edit_layers(2)
        randomint = random.randint(0, 3*3*2)
        test_section.paint_tile(randomint, 2)
        self.assertEqual(test_section.data[randomint], 2)

    def test_section_error_handling(self):
        pass


if __name__ == '__main__':
    unittest.main()
