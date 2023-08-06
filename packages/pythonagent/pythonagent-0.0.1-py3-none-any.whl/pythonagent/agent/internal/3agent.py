
from __future__ import unicode_literals
import logging
from pythonagent.lib import get_ident
import configparser
import ctypes
import os
import sys
import cProfile
import threading
import pstats
from collections import Counter
from pyclbr import readmodule
from pythonagent.agent.probes.frameworks import wsgi# aiflagset
#from guppy import hpy
#from pythonagent.agent.internal.profile import profile
#import pythonagent.main.pytrace.pytrace

"""def startaisession(a,b,c,d):
        print("*****")"""


class Agent(object):
    """The entry point for the Python agent.

    """

    def __init__(self):
        super(Agent, self).__init__()
        self.logger = logging.getLogger('pythonagent.agent')
        self.aiobj = None
        #if os.environ['CAV_RUNNING_MODE']=='0':
        #    os.environ['CAV_RUNNING_MODE']='1'
        #    return
        self.app_id = None
        self.tier_id = None
        self.node_id = None
        self.account_guid = None
        self.controller_guid = None

        self._tx_factory = None

        # Services
        #self.proxy_control_svc = None
        #self.config_svc = None
        #self.tx_svc = None
        #self.snapshot_svc = None

        # Registries
        #self.naming_registry = None
        #self.bt_registry = None
        #self.backend_registry = None
        #self.error_config_registry = None
        #self.data_gatherer_registry = None

        self.active_bts = set()
        self.current_bts = {}
        self.eum_config = None

        self.nd_init_done = None
        self.last_forced_snapshot = 0
        #self.c_startaisession = None
        self.lib = None
        self.start()
        #Agent.static_ai_wrapper_begin(Agent.startaisession)
        self.ai_wrapper_begin()
        self.ai_wrapper_end()

        self.current_status_code = {}
    

    def start(self):
        path = '/usr/local/lib/libndsdk.so'
        #if os.environ['nd_init_done']=='1':
        #    print('=========================Agent instance already created ignore start() method============================')
        #    return 
        #__shared_instance = None
        #configParser = configparser.RawConfigParser()
        #configParser.read(r'config.txt')
        #path = configParser.get('SO_PATH', 'path')
        #path = '/usr/local/lib/libndsdk.so'
        #self.logger.info("going to load common lib in proxy.py")
        self.lib = self.load_common_lib(path)
        self.logger.info("going to start sdk_init()")
        self.sdk_init()
        self.logger.info("sdk_init() done")
        #self.nd_init_done = True
        os.environ['nd_init_done'] = '1'

    
    def stop(self):
        """Stop the agent from doing anything else.

        Ideally this will stop any interceptors from doing anything, it will
        disconnect all ties to the proxy etc etc.

        """
        self.nd_init_done = False
        os.environ['nd_init_done'] = '0'

    #@staticmethod
    def getInstance(self):
        """Static Access Method"""
        if self.start.__shared_instance is None:
            #Proxy()
            print('=========================Going to invoke start agent instance in getInstance============================')
            self.start()
        #return Proxy.__shared_instance
        return self.start.__shared_instance

    #@profile
    def load_common_lib(self,lib_path):
        #global lib
        #if os.environ.get('LD_PRELOAD') is None:
            #self.lib = ctypes.cdll.LoadLibrary(lib_path)
            #self.logger.exception("Could not found 'LD_PRELOAD' env variable!!,  kindly set before start the python agent !!") 
        #    os.environ['LD_PRELOAD'] = "/usr/local/lib/libapr-1.so /usr/local/lib/libwebsockets.so /usr/local/lib/libcrypto.so /usr/local/lib/libssl.so"   
            #break
        # sdk_init,sdk free
        # structure not required since they do not return or require any arguments.
        # Method_entry
        #print('Environemt variable value is: ', os.environ['LD_PRELOAD'])
        #print('lib path before going to call load lib is: ',lib_path) 

        self.lib = ctypes.cdll.LoadLibrary(lib_path)
        #self.lib.nd_init2.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.nd_method_entry.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.nd_method_exit.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        self.lib.nd_bt_begin.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.nd_bt_begin.restype = ctypes.c_void_p

        self.lib.nd_bt_end.argtypes = [ctypes.c_void_p,ctypes.c_int]
        self.lib.nd_bt_end.restype = ctypes.c_int

        self.lib.nd_bt_store.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        self.lib.nd_ip_db_callout_begin.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.nd_ip_db_callout_begin.restype = ctypes.c_void_p

        self.lib.nd_ip_db_callout_end.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.lib.nd_ip_db_callout_end.restype = ctypes.c_int

        self.lib.nd_ip_http_callout_begin.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.nd_ip_http_callout_begin.restype = ctypes.c_void_p

        self.lib.nd_ip_http_callout_end.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.lib.nd_ip_http_callout_end.restype = ctypes.c_int
        
        #self.lib.register_AI_end_callback.argtypes = [ctypes.c_char_p]

        CB_FTYPE_DOUBLE_DOUBLE = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_longlong, ctypes.c_longlong, ctypes.c_char_p)
        self.c_startaisession = CB_FTYPE_DOUBLE_DOUBLE(self.startaisession)
        
        ai_end_ftype = ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_char_p)
        self.c_endaisession = ai_end_ftype(self.endaisessioncc)        
       
        self.logger.info("load common lib -> lib.obj :{0}".format(self.lib))
        return self.lib


    #def startaisession(self,a,b,c,d):
    
    def ai_wrapper_begin(self):
        print("************************ callback registered ********************************************")
        #self.logger.info("start profiling ->lib.obj :{0}".format(self.lib))
        self.lib.register_AI_start_callback(self.c_startaisession)
        #self.ai_wrapper_end()

    def ai_wrapper_end(self):
        print("************************ callback registered for end ai ********************************************")
        #self.logger.info("start profiling ->lib.obj :{0}".format(self.lib))
        self.lib.register_AI_end_callback(self.c_endaisession)
    
    def startaisession(self, istart, startTime, duration, sname):
        #self.aiobj = cProfile.Profile()
        #self.aiobj.enable()
        print(" IN startaisession") 
        wsgi.aiflagset(istart, startTime, duration)
    
    def endaisessioncc(self, sname):
        print("in the end ai sessesion in python agent file$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
    #@profile
    def sdk_init(self):
        self.logger.info("sdk_init -> lib.obj :{0}".format(self.lib))
        self.lib.nd_init("python","cavlib")

    def sdk_free(self):
        self.logger.info("sdk_free -> lib.obj :{0}".format(self.lib))
        self.lib.nd_free()

    #@profile
    def method_entry(self, bt, method):
        self.logger.info("method entry -> lib.obj :{0}".format(self.lib))
        self.logger.info("method entry -> method name :{0}".format(method))
        # defer C.free(unsafe.Pointer(method_c))
        #method_bytes = bytes(method, 'utf-8')
        try:
            method_bytes = bytes(method, 'utf-8')
        except:
            method_bytes = bytes(method.encode("utf-8"))
        self.lib.nd_method_entry(bt, ctypes.c_char_p(method_bytes))

    #@profile
    def method_exit(self, bt, method):
        self.logger.info("load common lib -> lib.obj :{0}".format(self.lib))
        self.logger.info("method entry -> method name :{0}".format(method))
        # defer C.free(unsafe.Pointer(method_c))
        # method_bytes = bytes(method, 'utf-8')
        try:
            method_bytes = bytes(method, 'utf-8')
        except: 
            method_bytes = bytes(method.encode("utf-8"))
        self.lib.nd_method_exit(bt, ctypes.c_char_p(method_bytes))

    #@profile
    def start_business_transaction(self, bt_name, correlation_header):
        if os.environ['nd_init_done'] == '0':
            self.start()
        print("start_business_transaction ->")
        self.logger.debug(" start_business_transaction -> lib.obj {0}:".format(self.lib))
       # btname = bytes(bt_name, 'utf-8')
       # self.logger.info("btname type and value: {0} and {1}".format(type(btname), btname))
       # bt_name_c = ctypes.c_char_p(btname)
       # self.logger.info("bt_name_c value: {0}".format(bt_name_c))
       # correlation_header = bytes(correlation_header, 'utf-8')
       # correlation_header_c = ctypes.c_char_p(correlation_header)
        try:
           # self.logger.debug(" start_business_transaction -> lib.obj {0}:".format(self.lib))
            btname = bytes(bt_name, 'utf-8')
       # btname = bytes(bt_name.encode("utf-8"))
            self.logger.info("btname type and value: {0} and {1}".format(type(btname), btname))
            bt_name_c = ctypes.c_char_p(btname)
            self.logger.info("bt_name_c value: {0}".format(bt_name_c))
            correlation_header = bytes(correlation_header, 'utf-8')
       # correlation_header = bytes(correlation_header.encode("utf-8"))
            correlation_header_c = ctypes.c_char_p(correlation_header)
        except:
            btname = bytes(bt_name.encode("utf-8"))
            self.logger.info("btname type and value: {0} and {1}".format(type(btname), btname))
            bt_name_c = ctypes.c_char_p(btname)
            self.logger.info("bt_name_c value: {0}".format(bt_name_c))
            correlation_header = bytes(correlation_header.encode("utf-8"))
            correlation_header_c = ctypes.c_char_p(correlation_header)

        bt = self.lib.nd_bt_begin(bt_name_c, correlation_header_c)
        self.logger.info("bt datatype : {0}".format(type(bt)))
        print("btname value: {0}".format(btname))
        #print('-----------------\nCurrent heap memory stack for BT: ',bt_name,' is : ',hpy().heap())
        self.active_bts.add(bt)
        self.set_current_bt(bt)
        print("BT value of this txn: ",bt)
        return bt

    #@profile
    def end_business_transaction(self, bt):
        print("end_business_transaction--> BT: ",bt)
        self.logger.info('end_business_transaction--> lib variable in end txn: {0}'.format(self.lib))
        self.logger.info('At end_business_transaction bt value is {0}'.format(bt))
        statuscode = self.get_current_status_code()
        rc = self.lib.nd_bt_end(bt,statuscode)
        self.logger.info("nd_bt_end return value:  {0}".format(int(rc)))
        self.unset_current_bt()
        self.unset_current_status_code()
        self.active_bts.discard(bt)
        return int(rc)

    #@profile
    def store_business_transaction(self, bt, unique_bt_id):
        self.logger.info('lib variable in store business txn: {0}'.format(self.lib))
       # unique_bt_id_bytes = bytes(unique_bt_id, 'utf-8')
        try:
            unique_bt_id_bytes = bytes(unique_bt_id, 'utf-8')
        except:
           unique_bt_id_bytes = bytes(unique_bt_id.encode("utf-8"))

        bt_id_c = ctypes.c_char_p(unique_bt_id_bytes)
        self.lib.nd_bt_store(bt, bt_id_c)

    #@profile
    def db_call_begin(self, bt, db_host, db_query):
       #db_host_c = bytes(db_host, 'utf-8')
       #db_query_c = bytes(db_query, 'utf-8')
        try:
            db_host_c = bytes(db_host, 'utf-8')
            db_query_c = bytes(db_query, 'utf-8')
        except:
            db_host_c = bytes(db_host.encode("utf-8"))
            db_query_c = bytes(db_query.encode("utf-8"))

        ip_handle = self.lib.nd_ip_db_callout_begin(bt, ctypes.c_char_p(db_host_c), ctypes.c_char_p(db_query_c))
        return ip_handle

    #@profile    #@staticmethod
    def db_call_end(self, bt, ip_handle):
        rc = self.lib.nd_ip_db_callout_end(bt, ip_handle)
        return int(rc)

    #@profile  #@staticmethod
    def http_call_begin(self, bt, http_host, url):
       #host_bytes = bytes(http_host, 'utf-8')
       #url_bytes = bytes(url, 'utf-8')
        #print("http_call_begin bt ---------------------",bt)
        #print("http_call_begin http_host ---------------------",http_host)
        #print("http_call_begin url---------------------",url)

        try:
            host_bytes = bytes(http_host, 'utf-8')
            url_bytes = bytes(url, 'utf-8')
        except:
            host_bytes = bytes(http_host.encode("utf-8"))
       # url_bytes = bytes(url, 'utf-8')
            url_bytes = bytes(url.encode("utf-8"))

        handle = self.lib.nd_ip_http_callout_begin(bt, ctypes.c_char_p(host_bytes), ctypes.c_char_p(url_bytes))
        return handle

    #@profile #@staticmethod
    def http_call_end(self, bt, ip_handle):
        rc = self.lib.nd_ip_http_callout_end(bt, ip_handle)
        return int(rc)


    def wait_for_start(self, timeout_ms=None):
        """Wait for the agent to start and get configured.

        Other Parameters
        ----------------
        timeout_ms : int, optional
            The maximum time to wait for the agent to start and be configured
            before returning.

        Returns
        -------
        bool
            Returns ``True`` if the agent is enabled after waiting, else
            ``False``.

        """
        if timeout_ms is not None:
            with self.timer() as timer:
                if self.proxy_control_svc is not None:
                    self.proxy_control_svc.wait_for_start(timeout_ms=timeout_ms)

                if self.config_svc is not None:
                    timeout_ms = max(0, timeout_ms - timer.duration_ms)
                    self.config_svc.wait_for_config(timeout_ms=timeout_ms)

                if self.tx_svc is not None:
                    timeout_ms = max(0, timeout_ms - timer.duration_ms)
                    self.tx_svc.wait_for_start(timeout_ms=timeout_ms)
        else:
            self.proxy_control_svc.wait_for_start()
            self.config_svc.wait_for_config()
            self.tx_svc.wait_for_start()

        return self.enabled

    def wait_for_end(self, timeout_ms=None):
        """Wait for the agent to finish reporting any pending BTs.

        """
        self.tx_svc.wait_for_end(timeout_ms=timeout_ms)

    #@property
    def enabled(self):
        """Return true if the agent has started and is enabled.

        """
        return (
                self.nd_init_done and
                self.config_svc and self.config_svc.enabled and
                self.tx_svc)



    def get_current_bt(self):
        """Get the currently active BT for the calling context.

        The calling context is the active greenlet or thread, depending on
        whether greenlets are in use or not. If the agent is disabled, or if
        there is no active transaction for the calling context, None is
        returned.

        Returns
        -------
        bt : appdynamics.agent.core.bt.Transaction or None
            the active business transaction (if any)

        """
        #if not self.enabled:
        #    return None
        return self.current_bts.get(get_ident(), None)

    def set_current_bt(self, bt):
        if bt:
            self.current_bts[get_ident()] = bt

    def unset_current_bt(self):
        self.current_bts.pop(get_ident(), None)
    
    def get_current_status_code(self):
        return self.current_status_code.get(get_ident(), None)

    def set_current_status_code(self, status_code):
        if status_code:
            self.current_status_code[get_ident()] = status_code

    def unset_current_status_code(self):
        self.current_status_code.pop(get_ident(), None)
 
   
    '''
    @staticmethod
    def start_exit_call(bt, start_frame_info, backend, **kwargs):
        """Start an exit call, taking a sample if the BT is snapshotting.

        """
        exit_call = bt.start_exit_call(start_frame_info, backend, **kwargs)
        if exit_call and bt.snapshotting:
            bt.sample_data.take_outer_frames(exit_call.timer.start_time_ms, bt.active_exit_calls)
        return exit_call

    @staticmethod
    def end_exit_call(bt, exit_call, end_frame_info, exc_info=None):
        """End an exit call.

        """
        bt.end_exit_call(exit_call, end_frame_info, exc_info=exc_info)

    def end_transaction(self, bt):
        """End the active transaction on this thread.

        Parameters
        ----------
        exc_info : (exc_type, exc_value, exc_tb) or None
            If an uncaught exception caused the transaction to end, then this
            contains the exception info (as returned by `sys.exc_info()`). If
            no exception occurred, then `None`.

        bt : appdynamics.agent.models.transactions.Transaction, optional
            A specific BT to end.

        """
        self.unset_current_bt()
        self.active_bts.discard(bt)
        if self.enabled and bt:
            self.stall_monitor_svc.end_bt_monitor(bt)
            self.tx_svc.end_transaction(bt)

    def end_active_bts(self):
        """End all the active BTs.

        """
        for bt in self.active_bts:
            self.end_transaction(bt)


    def report_custom_metric(self, metric, value):
        if not self.started:
            raise AgentNotStartedException

        if not self.enabled:
            raise AgentNotReadyException

        self.tx_svc.report_custom_metric(metric, value)
    '''


class AgentNotStartedException(Exception):
    pass


class AgentNotReadyException(Exception):
    pass


class IgnoreTransaction(Exception):
    pass

