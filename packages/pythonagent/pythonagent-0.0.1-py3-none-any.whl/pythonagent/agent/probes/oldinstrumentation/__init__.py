from ..base import ExitCallInterceptor
from pythonagent.agent.probes.Instrumentation.parser import create_method_array
import os
import configparser
#configParser = configparser.RawConfigParser()
path = os.environ.get('ND_HOME')
path = path + '/config/ndsettings.conf'
print("path of  NDC config : ",path )
#configParser.read(path)
#path_for_insProfile = configParser.get('PYTHON_AGENT', 'path_profile')
myvars = {}
with open(r"/opt/cavisson/netdiagnostics/config/ndsettings.conf") as myfile:
    for line in myfile:
        name, var = line.partition("=")[::2]
        myvars[name.strip()] = var
try:
    path_for_insProfile = myvars.get('path_profile').strip('\n')
except:
    #path_for_insProfile= os.environ.get('ND_HOME') + "/CavAgent/instrumentationprofile.txt"
    path_for_insProfile= os.environ.get('ND_HOME') + "/CavAgent/instrumentationprofile.json"
print('Profiler path at : ',path_for_insProfile)
#custom_methods_to_instrument = create_method_array('/home/cavisson/shop/my-shop/instrumentationprofile.txt')
custom_methods_to_instrument = create_method_array(path_for_insProfile)
print("ALL custom modules(instrument)-> ",custom_methods_to_instrument)





class MethodInterceptor(ExitCallInterceptor):


    def _custom_method(self, original_method, *args, **kwargs):
        print("\n\n\n\n\n\n")
        print("Custom Method:",original_method)
        print("\n\n\n\n\n\n")
        bt = self.bt
        self.agent.logger.info("Modulename: MethodInterceptor class inside _custom_method bt value is {0}".format(bt))
        self.agent.logger.info("Modulename: MethodInterceptor class inside _custom_method original_method is {0}".format(original_method))

        method = None
        if bt is not None:
            try:
                print("calling original method....", original_method.__name__)
                # method = self.proxy.method_entry(bt, original_method.__name__)
                self.agent.logger.info("Modulename: MethodInterceptor class inside _custom_method original_method.__name__ is {0}".format(original_method.__name__))

                method = self.agent.method_entry(bt, original_method.__name__)
                original_method(*args, **kwargs)
                print("called original method....")
                self.agent.logger.info('Modulename: MethodInterceptor class inside _custom_method orginal method called')

            except:
                print("got an exception in _custom_method")
                self.agent.logger.exception('Modulename: MethodInterceptor class inside _custom_method got exception in orginal method')

            finally:
                print("\n\n\ninsidefinally....", original_method.__name__)
                if method is not None:
                    print("\n\n\ninsidefinallyif....", original_method.__name__)
                    self.agent.method_exit(bt, method)
        else:
            self.agent.logger.info("did not find BT in ModuleInterceptor._custom_method")
            self.agent.logger.exception('Modulename: MethodInterceptor class inside _custom_method,,did not find BT in ModuleInterceptor._custom_method')
            original_method(*args, **kwargs)



















def intercept_instrumented_method(agent, mod):


    print("\n\n\n\n\n\n")
    print("Intercept Intrumented Method")
    print("\n\n\n\n\n\n")


    for item in custom_methods_to_instrument:
        

        #print("item name in custom_methods_to_intercept",item)
        agent.logger.info("Modulename: MethodInterceptor class inside intercept_instrumented_method item name in custom_methods_to_intercept {0}".format(item))
        check = item.split(".")
        #print("array after split: ",check)
        if len(check) == 2:
            try:
                MethodInterceptor(agent, mod).attach(check[1],patched_method_name='_custom_method')
            except:
                agent.logger.debug("Instrumentation.__init__: class ".format(check[1])+" not present in module")
                agent.logger.exception('Modulename: MethodInterceptor class inside intercept_instrumented_method,Instrumentation.__init__: class ",check[1]," not present in module')

                continue    
               #MethodInterceptor(agent, mod).attach(check[1],wrapper_func='_custom_method')
        if len(check) == 3:
            #MethodInterceptor(agent, getattr(mod, check[1])).attach(check[2],wrapper_func='_custom_method')
            try: 
                MethodInterceptor(agent, getattr(mod, check[1])).attach(check[2],patched_method_name='_custom_method')
            except:
                agent.logger.exception('Modulename: MethodInterceptor class inside intercept_instrumented_method, Instrumentation.__init__: method /class: ",check[1],".",check[2]," not present in module"')
                agent.logger.debug("Instrumentation.__init__: method /class: ".format(check[1])+".".format(check[2])+" not present in module")
                continue

