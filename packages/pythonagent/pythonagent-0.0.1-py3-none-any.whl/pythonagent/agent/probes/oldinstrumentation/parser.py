import json

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

local = False


def create_module_array(filePath):
    lines = []

    with open(filePath, 'r') as file_handle:
        for line in file_handle:
            line = line[:-1]  # remove newline character
            lines.append(line)

    # list of methods
    list_of_modules = []
    for line in lines:
        split_line = line.split("|")
        modules = split_line[0]
        methods_split = modules.split(".")
        module_name = methods_split[0]

        if module_name not in list_of_modules:
            list_of_modules.append(module_name)

    arr = [str(r) for r in list_of_modules]
    return arr


def create_method_array(filePath):

    lines = []

    with open(filePath, 'r') as file_handle:
        for line in file_handle:
            line = line[:-1]  # remove newline character
            lines.append(line)

    # list of methods
    list_of_methods = []
    print(lines)

    for line in lines:
        print("\n\n\n")
        print(line)
        print("\n\n\n")
        split_line = line.split("|")
        print("\n\n\n")
        print(split_line)
        print("\n\n\n")
        base = split_line[0]
        methods = split_line[1]
        if methods:
            methods_split = methods.split(",")
            for item in methods_split:
                string = base + '.' + item
                list_of_methods.append(string)

    arr = [str(r) for r in list_of_methods]

    return arr


if local:
    path = "/tmp/CavAgent/instrumentationprofile.txt"
    abc = create_method_array(path)
    abc = create_module_array(path)
    print(abc)
