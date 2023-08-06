import os
import ast
import json
import ctypes
import sys
import time

local = False
lib_path = '/usr/local/lib/libndsdk.so'
basic_function_lib = None

try:
    basic_function_lib = ctypes.cdll.LoadLibrary(lib_path)
except:
    print("OS %s not recognized" % sys.platform)

def find(path):
    print("Instrumentation started")
    #path = "/home/cavisson/pythonagent"
    modules = []
    default_path = []
    for root, dirs, files in os.walk(path):
        for file in files:
            # print(file)
            if file.endswith(".py"):
                default_path.append(os.path.join(root, file))
                file = file[:-3]  # Remove .py extension
                modules.append(file)

    path_module_dict = dict(zip(default_path, modules))
    profile = []

    for filename in default_path:
        module = path_module_dict[filename]

        # Create list of class level methods
        classes = []
        for n in ast.parse(open(filename).read()).body:
            if isinstance(n, ast.ClassDef):
                classes.append(n)

        for cname in classes:
            clms = []
            for n in cname.body:
                if isinstance(n, ast.FunctionDef):
                    clms.append(n)

            # Create new string for profile (one for each class)
            p_string = module + "." + cname.name + "|"

            for clm in clms:
                p_string = p_string + clm.name + ","

            if clms:  # If list not empty
                p_string = p_string[:-1]  # Remove final comma

            profile.append(p_string)

        # Create list of module level methods

        mlms = []

        for n in ast.parse(open(filename).read()).body:
            if isinstance(n, ast.FunctionDef):
                mlms.append(n)

        # Create new string for profile (one for each module)
        p_string = module + "|"

        for mlm in mlms:
            p_string = p_string + mlm.name + ","

        if mlms:  # If list not empty
            p_string = p_string[:-1]  # Remove final comma

        profile.append(p_string)

    # for x in profile:
    #     print(x)

    with open("/opt/cavisson/netdiagnostics/CavAgent/instrumentationprofile.txt", "w") as outfile:
        for item in profile:
            outfile.write('%s\n' % item)

# CALLBACK STUFF

"""
# Type Definition for ad_callback
typedef void (*ad_callback)(char *methodFiltersPatternList[], char *classFiltersPatternList[], int msize, int csize);

# Pointer to function of type ad_callback
ad_callback ad_callback_func = NULL;

void register_AD_callback(ad_callback adfunc)
{
  ad_callback_func = adfunc;
}
"""

# Define C Pointer to a function Type
#CB_PTR_FTYPE = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)

# Define a C function equivalent to the python function "find"
#cb_find = CB_PTR_FTYPE(find)

# C Code about the C function
#basic_function_lib.register_AD_callback(cb_find)
