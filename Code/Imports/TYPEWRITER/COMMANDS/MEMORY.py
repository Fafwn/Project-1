"""

"""

import csv


def __init__(self):
    flag = {}
    var = {}
    create_memory(read_CSV("FLAGS.CSV"))


def update_flag():
    pass


def update_var():
    pass


def read_CSV(file):
    with open(file, "r") as raw:
        return [x for x in csv.reader(raw, delimiter=",")]


def create_memory(arr):
    [flag.update({x[0]: bool(int(x[2]))}) for x in arr if x[1] == "!"]
    [var.update({x[0]: x[2]}) for x in arr if x[1] == "?"]


if __name__ == "__main__":
    flag = {}
    var = {}
    create_memory(read_CSV("FLAGS.CSV"))
    print("%s%s" % (flag, var))
