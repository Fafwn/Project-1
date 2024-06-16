"""

"""

import csv

parentDir = ""
flags = ""
flag = {}
var = {}


def read_CSV(file):
    with open("%s%s" % (parentDir, flags), "r") as raw:
        return [x for x in csv.reader(raw, delimiter=",")]


def create_memory(arr):
    [flag.update({x[0]: bool(int(x[2]))}) for x in arr if x[1] == "!"]
    [var.update({x[0]: x[2]}) for x in arr if x[1] == "?"]


if __name__ == "__main__":
    parentDir = ""
    flags = "FLAGS.CSV"
    create_memory(read_CSV(flags))
    #print(memory["gameBegin"])
