import configparser
import ctypes


def load_common_lib(lib_path):
    global lib
    lib = ctypes.cdll.LoadLibrary(lib_path)
    # global lib
    # sdk_init,sdk free
    # structure not required since they do not return or require any arguments.
    # Method_entry
    lib.nd_method_entry.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    lib.nd_method_exit.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    lib.nd_bt_begin.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.nd_bt_begin.restype = ctypes.c_void_p

    lib.nd_bt_end.argtypes = [ctypes.c_void_p]
    lib.nd_bt_end.restype = ctypes.c_int

    lib.nd_bt_store.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    lib.nd_ip_db_callout_begin.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
    lib.nd_ip_db_callout_begin.restype = ctypes.c_void_p

    lib.nd_ip_db_callout_end.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    lib.nd_ip_db_callout_end.restype = ctypes.c_int

    lib.nd_ip_http_callout_begin.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
    lib.nd_ip_http_callout_begin.restype = ctypes.c_void_p

    lib.nd_ip_http_callout_end.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    lib.nd_ip_http_callout_end.restype = ctypes.c_int

    print("load common lib -> lib.obj :", lib)
    return lib

def sdk_init():
    print("sdk_init -> lib.obj :", lib)
    lib.nd_init()


def sdk_free():
    print("sdk_free -> lib.obj :", lib)
    lib.nd_free()

class Proxy:
    __shared_instance = None
    configParser = configparser.RawConfigParser()
    configParser.read(r'config.txt')
    path = configParser.get('SO_PATH', 'path')
    print("going to load common lib in proxy.py")
    lib = load_common_lib(path)
    print("going to start sdk_init()")
    sdk_init()
    print("sdk_init() done")

    @staticmethod
    def getInstance():
        """Static Access Method"""
        if Proxy.__shared_instance is None:
            Proxy()
        return Proxy.__shared_instance

    def __init__(self):

        """virtual private constructor"""
        if Proxy.__shared_instance is not None:
            raise Exception("This class is a Proxy class !")
        else:
            Proxy.__shared_instance = self

    def method_entry(self,bt, method):
        print("method entry -> lib.obj :",self.lib)
        # defer C.free(unsafe.Pointer(method_c))
        method_bytes = bytes(method, 'utf-8')
        self.lib.nd_method_entry(bt, ctypes.c_char_p(method_bytes))

    def method_exit(self,bt, method):
        print("load common lib -> lib.obj :",self.lib)
        # defer C.free(unsafe.Pointer(method_c))
        method_bytes = bytes(method, 'utf-8')
        self.lib.nd_method_exit(bt, ctypes.c_char_p(method_bytes))

    def start_business_transaction(self,bt_name, correlation_header):
        
        print(" start_business_transaction -> lib.obj :",self.lib)
        btname = bytes(bt_name, 'utf-8')
        print("btname type and value: ", type(btname), btname)
        bt_name_c = ctypes.c_char_p(btname)
        print("bt_name_c value: ",bt_name_c)
        correlation_header = bytes(correlation_header, 'utf-8')
        correlation_header_c = ctypes.c_char_p(correlation_header)
        #print("correlation_header_c value: ",correlation_header_c)
        # defer C.free(unsafe.Pointer(bt_name_c))
        # defer C.free(unsafe.Pointer(correlation_header_c))
        bt = self.lib.nd_bt_begin(bt_name_c, correlation_header_c)
        print ("bt datatype :",type(bt))
        return bt

    def end_business_transaction(self,bt):
        print('lib variable in end txn: ', self.lib)
        rc = self.lib.nd_bt_end(bt)
        print("nd_bt_end return value: ", int(rc))
        return int(rc)

    def store_business_transaction(self,bt, unique_bt_id):
        print('lib variable in store business txn: ', self.lib)
        unique_bt_id_bytes = bytes(unique_bt_id, 'utf-8')
        # print("unique_bt_id_bytes value: ",unique_bt_id_bytes)
        bt_id_c = ctypes.c_char_p(unique_bt_id_bytes)
        # print("bt_id_c value: ",bt_id_c)
        self.lib.nd_bt_store(bt, bt_id_c)

    def db_call_begin(self,bt, db_host, db_query):
        db_host_c = bytes(db_host, 'utf-8')
        db_query_c = bytes(db_query, 'utf-8')
        # print(">>>>>>>db_call_begin host: ",db_host_c, "value: ", db_host," db_query: ",db_query_c," value: ",db_query)
        ip_handle = lib.nd_ip_db_callout_begin(bt, ctypes.c_char_p(db_host_c), ctypes.c_char_p(db_query_c))
        # print("db_call_begin: ip handle: ",type(ip_handle)," value: ",ip_handle)
        return ip_handle

    def db_call_end(self,bt, ip_handle):
        rc = lib.nd_ip_db_callout_end(bt, ip_handle)
        return int(rc)

    def http_call_begin(self,bt, http_host, url):
        host_bytes = bytes(http_host, 'utf-8')
        url_bytes = bytes(url, 'utf-8')
        handle = lib.nd_ip_http_callout_begin(bt, ctypes.c_char_p(host_bytes), ctypes.c_char_p(url_bytes))
        return handle

    def http_call_end(self,bt, ip_handle):
        rc = lib.nd_ip_http_callout_end(bt, ip_handle)
        return int(rc)


# main method
# if __name__ == "__main__":
#     # create object of Proxy Class
#     obj = Proxy()
#     print(obj)
#
#     # pick the instance of the class
#     obj = Proxy.getInstance()
#     print(obj)

