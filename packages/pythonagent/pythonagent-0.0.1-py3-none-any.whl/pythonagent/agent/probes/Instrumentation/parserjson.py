import json
#import jsonpickle
#from json import JSONEncoder

from json.scanner import py_make_scanner
from json.decoder import JSONArray

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

class MasterObj(object):
    def __init__(self,modules):
        self.modules = modules

class Module(object):
    def __init__(self,moduleLevelMethod,classes,name):
        self.name = name
        self.moduleLevelMethod = moduleLevelMethod
        self.classes = classes
        
class Method(object):
    def __init__(self,name,signature):
        self.name = name
        self.signature = signature

class Class(object):
    def __init__(self,methods,className):
        self.className = className
        self.methods = methods



#m1 = Method("method1","NA")
#m2 = Method("method2","NA")
#classLevelMethods = [m1,m2]
#class1 = Class(classLevelMethods,"classname1")
#classes = [class1]
#moduleLevelMethod = [m1,m2]
#mod1 = Module(moduleLevelMethod,classes,"https")
#modules = [mod1]
#student = MasterObj(modules)

#print("Encode Object into JSON formatted Data using jsonpickle")


def flatten_hook(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            try:
                obj[key] = json.loads(value, object_hook=flatten_hook)
            except ValueError:
                pass
    return obj




#studentJSON = jsonpickle.encode(student)
#print(studentJSON)

#json1 = json.loads(studentJSON,object_hook=flatten_hook)
#print("Decode and Convert JSON into Object using object_hook")
#print(json1)
#print("Object type is: ", type(json1))
#json2 = r"""{
#  "modules": [
#    {
#      "moduleName": "https",
#      "moduleLevelMethod": [
#      {
#        "name":"method1",
#        "signature":"NA"
#      },
#      {
#        "name":"method2",
#        "signature":"NA"
#      }
#      ],
#      "classes": [
#        {
#          "className": "BaseInterceptor",
#          "classLevelMethods": [
#      {
#        "name":"classmethod1",
#        "signature":"NA"
#      },
#      {
#        "name":"classmethod2",
#        "signature":"NA"
#      }
#      ]
#        }
#      ]
#    }
#  ]
#}
# """

def create_method_json(filePath):
    f = open(filePath, "r")
    obj2 = json.loads(f.read(),object_hook=flatten_hook)
    print("\n\n\n")
    print(obj2)
    print("\n\n\n")


    return obj2


def _parse_constant(arg):
    print("got:", arg)
    c = {"-Infinity": "-Infinity",
         "Infinity": "Infinity",
         "NaN": "NaN"
         }
    return c[arg]

def create_method_array(filePath):
    print("hi\n\n\n\n\n\n\n\n\n\n")
    f = open(filePath, "r")
    #obj2 = json.loads(f.read(),object_hook=flatten_hook,parse_constant=test)
    x = f.read()
    print(x)
    print(type(x))

    obj2 = json.loads(x, parse_constant=_parse_constant)

    print(obj2)

    #list of methods
    LOM = []

    for module in obj2["modules"]:

        # module = module.split("/")[-1].replace(".py","")
        # print(module+"--------------------------------------------")
        for MLM in module["moduleLevelMethod"]:
            print(module["moduleName"])
            LOM.append(module["moduleName"] + "." + MLM["name"])
        for each_class in module["classes"]:
            for CLM in each_class["classLevelMethods"]:

                print(module["moduleName"], type(module["moduleName"]))
                print(each_class["className"], type(each_class["className"]))
                print(CLM["name"], type(CLM["name"]))
                print("\n\n")
                LOM.append(module["moduleName"] + "." + each_class["className"] + "." + CLM["name"])

    # print(LOM)

    arr = [str(r) for r in LOM]

    # print(arr)
    return arr

# abc = create_method_json("/home/cavisson/pythonagent/agent/probes/Instrumentation")["modules"]

#print("helloworld")
#abc = create_method_array("/home/cavisson/pythonagent/agent/probes/Instrumentation/d.json")
#print(abc)
# print(abc["moduleName"])

