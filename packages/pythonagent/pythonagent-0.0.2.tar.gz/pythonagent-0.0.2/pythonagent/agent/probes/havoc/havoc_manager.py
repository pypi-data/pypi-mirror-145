import json
from collections import namedtuple
import time
import logging
from pythonagent.agent.internal import udp
from pythonagent.agent.probes.havoc.havoc_constants import HAVOC_TYPES, EXPIRE_DURATION_MS, SIZE_OF_OBJECTS_BYTES, HAVOC_PROFILES_JSON

havoc_types = {
    1: "InBoundService_Delay",
    2: "InBoundService_Failure",
    3: "OutBoundService_Delay",
    4: "OutBoundService_Failure",
    5: "MethodCall_Delay",
    6: "MethodCall_Failure"
}

class NDHavocException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NDNetHavocRequest(object):
    def __init__(self, havoc_conf, header_dict):

        if hasattr(havoc_conf, 'havocType'):
            self.havocType = havoc_conf.havocType

        if hasattr(havoc_conf, 'uRL'):
            self.uRL = havoc_conf.uRL

        if hasattr(havoc_conf, 'methodFQM'):
            self.methodFQM = havoc_conf.methodFQM

        if hasattr(havoc_conf, 'delayInSec'):
            # self.delayInSec = havoc_conf.delayInSec
            self.delayInSec = havoc_conf.delayInSec / 1000  # UI is sending in milliseconds


        if hasattr(havoc_conf, 'hostname'):
            self.hostname = havoc_conf.hostname

        self.startTime = time.time_ns() // 1000000
        self.header_dict = header_dict
        self.totalDurationInSec = havoc_conf.totalDurationInSec

        try:
            self.enable = havoc_conf.enable
            self.bTName = havoc_conf.bTName
            self.isHavocEnable = False
            self.threshOld = havoc_conf.threshOld
            self.protocol = havoc_conf.protocol
            self.leaksINMB = havoc_conf.leaksINMB
            self.memoryLeaksInSec = havoc_conf.memoryLeaksInSec
            self.backendName = havoc_conf.backendName

        except Exception as e:
            print(e)
            pass




class NDNetHavocMonitor(object):

    __instance = None

    @staticmethod
    def get_instance():
        if NDNetHavocMonitor.__instance == None:
            NDNetHavocMonitor()
        return NDNetHavocMonitor.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if NDNetHavocMonitor.__instance != None:
            raise Exception("This class is a singleton! Use get_instance()")
        else:
            NDNetHavocMonitor.__instance = self

            self.enableNetHavoc = False

            self.netHavocConfigMap = {
                "InBoundService_Delay": [],
                "InBoundService_Failure": [],
                "OutBoundService_Delay": [],
                "OutBoundService_Failure": [],
                "MethodCall_Delay": [],
                "MethodCall_Failure": []
            }

            self.is_parsed = False
            self.logger = logging.getLogger('pythonagent.agent')


    def set_enable_net_havoc(self, enable_logs_net_havoc):
        try:
            if enable_logs_net_havoc == 1:
                self.enableNetHavoc = True
            else:
                self.enableNetHavoc = False
        except Exception as e:
            raise e

    def validate_config(self, havoc_conf):
        print("\n\n\n VALIDATING \n\n\n")
        self.logger.info("Validating config")
        is_valid = False

        # Validate enable
        if not hasattr(havoc_conf, 'enable'):
            return_message = "enable not found"
            return is_valid, return_message

        else:
            if havoc_conf.enable not in [0, 1]:
                return_message = "invalid enable not found"
                return is_valid, return_message
            else:
                logging.debug("enable validated")

        # Validate havocType
        if not hasattr(havoc_conf, 'havocType'):
            return_message = "havocType not found"
            return is_valid, return_message
        else:
            if havoc_conf.havocType not in [1, 2, 3, 4, 5, 6, 7, 8]:
                return_message = "invalid havocType"
                return is_valid, return_message
            else:
                havoc_type = havoc_conf.havocType
                logging.debug("havocType validated")

        # Validate totalDurationInSec
        if not hasattr(havoc_conf, 'totalDurationInSec'):
            return_message = "totalDurationInSec not found"
            return is_valid, return_message
        else:
            if not isinstance(havoc_conf.totalDurationInSec, int):
                return_message = "invalid totalDurationInSec"
                return is_valid, return_message
            else:
                logging.debug("totalDurationInSec validated")

        # Validate threshOld
        if not hasattr(havoc_conf, 'threshOld'):
            return_message = "threshOld not found"
            return is_valid, return_message
        else:
            if not hasattr(havoc_conf.threshOld, 'percentage'):
                return_message = "invalid threshOld"
                return is_valid, return_message
            else:
                self.logger.debug("threshOld validated")

        # Validate uRL
        if havoc_type in [1, 2]:
            if not hasattr(havoc_conf, 'uRL'):
                return_message = "uRL not found for inbound service"
                return is_valid, return_message
            else:
                if len(havoc_conf.uRL) == 0:
                    return_message = "invalid uRL  for inbound service"
                    return is_valid, return_message
                else:
                    self.logger.debug("uRL validated")
        else:
            self.logger.debug("uRL not needed")

        # Validate hostname and protocol
        if havoc_type in [3, 4]:
            if not hasattr(havoc_conf, 'hostname'):
                return_message = "hostname not found for outbound service"
                return is_valid, return_message
            else:
                if len(havoc_conf.hostname) == 0:
                    return_message = "invalid hostname for outbound service"
                    return is_valid, return_message
                else:
                    self.logger.debug("hostname validated")

                if not hasattr(havoc_conf, 'protocol'):
                    if havoc_conf.protocol not in ["Http", "Non Http"]:
                        return_message = "invalid protocol for outbound service"
                        return is_valid, return_message
                    else:
                        self.logger.debug("protocol validated")
                else:
                    self.logger.debug("protocol not found")
        else:
            self.logger.debug("hostname not needed")

        # Validate methodFQM
        if havoc_type in [5, 6]:
            if not hasattr(havoc_conf, 'methodFQM'):
                return_message = "methodFQM not found for method"
                return is_valid, return_message
            else:
                if len(havoc_conf.methodFQM) == 0:
                    return_message = "invalid methodFQM for method"

                    return is_valid, return_message
                else:
                    self.logger.debug("methodFQM validated")
        else:
            self.logger.debug("methodFQM not needed")

        if havoc_type in [1, 3, 5]:
            if not hasattr(havoc_conf, 'delayInSec'):
                return_message = "delayInSec not found for delay"
                return is_valid, return_message
            else:
                if not isinstance(havoc_conf.delayInSec, int):
                    return_message = "invalid delayInSec for delay"
                    return is_valid, return_message
                else:
                    self.logger.debug("delayInSec validated")
        else:
            self.logger.debug("delayInSec not needed")

        # 1.InBoundServicdelayhavoc
        # 2.InBoundServicefailhavoc
        # 3.OutBoundServicedelayhavoc
        # 4 OutBoundServicefailhavoc
        # 5.MethoCalldelayHavoc
        # 6.MethodInvocationfailhavoc
        # 7.Increasememoryusagehavoc
        # 8.IncreaseCPUutilization

        is_valid = True
        return_message = "Config Validated"
        return is_valid, return_message

    # def parse_nethavoc_config(self, json_conf, havoc_type, header_dict):
    def parse_nethavoc_config(self, json_conf, header_dict):
        self.logger.info("Parsing config")

        try:
            havoc_conf = json.loads(json_conf, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            havoc_type = havoc_conf.havocType
            self.logger.info("Havoc type: {}".format(havoc_type))

            is_valid, ret_message = self.validate_config(havoc_conf)

            if is_valid:
                self.logger.info(ret_message)
                req_obj = NDNetHavocRequest(havoc_conf, header_dict)
                self.is_parsed = True

                havoc_type_full_str = havoc_types[havoc_type]
                self.netHavocConfigMap[havoc_type_full_str].append(req_obj)
                # self.netHavocConfigMap[havoc_type].append(req_obj)

            else:
                self.logger.warning("Invalid config: {}".format(ret_message))

        except Exception as e:
            raise e

        return self.is_parsed

    def common_delay_in_response(self, total_duration_in_sec):
        self.logger.info("Applying delay duration(sec): {}".format(total_duration_in_sec))
        try:
            time.sleep(total_duration_in_sec)
        except Exception as e:
            raise e

    def common_failure(self, exception_message):
        self.logger.info("Applying failure message: {}".format(exception_message))

        raise NDHavocException(exception_message)

    @staticmethod
    def create_dummy_object(obj_size):
        int_list_size = obj_size // 4  # Size of int = 4
        obj = []
        for i in range(int_list_size):
            obj.append(i)
        return obj

    def memory_leak(self, leaksINMB, memoryLeaksInSec):

        total_leak_bytes = leaksINMB * 1024 * 1024
        num_of_obj = total_leak_bytes // SIZE_OF_OBJECTS_BYTES
        time_for_each_obj = memoryLeaksInSec // num_of_obj

        obj_created = 0
        while obj_created < num_of_obj:
            self.create_dummy_object(SIZE_OF_OBJECTS_BYTES)
            time.sleep(time_for_each_obj)
            obj_created += 0

    def apply_inbound_service_delay(self, req_url):
        self.logger.info("applying inbound service delay")
        config_list = self.netHavocConfigMap["InBoundService_Delay"]

        if config_list:
            for config in config_list:
                url = config.uRL
                delay_in_second = config.delayInSec

                # if url == req_url:
                if url in req_url:
                    self.logger.debug("Config matched for Request URL {}".format(req_url))
                    self.common_delay_in_response(delay_in_second)
                else:
                    self.logger.debug("Config not matched for Request URL {}".format(req_url))
        else:
            self.logger.warning("config not set for apply_inbound_service_delay")
            # raise Exception("config not set for apply_inbound_service_delay")

    def apply_inbound_service_failure(self, req_url):
        self.logger.info("applying inbound service failure")
        config_list = self.netHavocConfigMap["InBoundService_Failure"]

        if config_list:
            for config in config_list:
                url = config.uRL

                # if url == req_url:
                if url in req_url:
                    self.logger.debug("Config matched for Request URL {}".format(req_url))
                    self.common_failure(url)  # CHECK ARGUMENT
                else:
                    self.logger.debug("Config not matched for Request URL {}".format(req_url))

        else:
            self.logger.warning("config not set for apply_inbound_service_failure")
            # raise Exception("config not set for apply_inbound_service_failure")

        pass

    def apply_outbound_service_delay(self, req_hostname):
        self.logger.info("applying outbound service delay")
        config_list = self.netHavocConfigMap["OutBoundService_Delay"]

        if config_list:
            for config in config_list:
                hostname = config.hostname
                delay_in_second = config.delayInSec

                # if hostname == req_hostname:
                if hostname in req_hostname:

                    self.logger.debug("Config matched for Request Hostname {}".format(req_hostname))
                    self.common_delay_in_response(delay_in_second)
                else:
                    self.logger.debug("Config not matched for Request Hostname {}".format(req_hostname))
        else:
            self.logger.warning("config not set for apply_outbound_service_delay")
            # raise Exception("config not set for apply_outbound_service_delay")

    def apply_outbound_service_failure(self, req_hostname):
        self.logger.info("applying outbound service failure")
        config_list = self.netHavocConfigMap["OutBoundService_Failure"]

        if config_list:
            for config in config_list:
                hostname = config.hostname

                # if hostname == req_hostname:
                if hostname in req_hostname:

                    self.logger.debug("Config matched for Request Hostname {}".format(req_hostname))
                    self.common_failure(hostname)  # CHECK ARGUMENT
                else:
                    self.logger.debug("Config not matched for Request Hostname {}".format(req_hostname))

        else:
            self.logger.warning("config not set for apply_outbound_service_failure")
            # raise Exception("config not set for apply_outbound_service_failure")

    def apply_method_call_delay(self, req_method_fqm):
        self.logger.info("applying method call delay")
        config_list = self.netHavocConfigMap["MethodCall_Delay"]

        if config_list:
            for config in config_list:
                delay_in_second = config.delayInSec
                method_fqm = config.methodFQM

                print("\n\nmethod_fqm == req_method_fqm", method_fqm, req_method_fqm)

                # if method_fqm == req_method_fqm:
                if method_fqm in req_method_fqm:
                    self.logger.debug("Config matched for Request FQM {}".format(req_method_fqm))
                    self.common_delay_in_response(delay_in_second)
                else:
                    self.logger.debug("Config not matched for Request FQM {}".format(req_method_fqm))
        else:
            self.logger.warning("config not set for apply_method_call_delay")
            # raise Exception("config not set for apply_method_call_delay")

    def apply_method_invocation_failure(self, req_method_fqm):
        self.logger.info("applying method invocation failure")
        config_list = self.netHavocConfigMap["MethodCall_Failure"]

        if config_list:
            for config in config_list:
                method_fqm = config.methodFQM

                # if method_fqm == req_method_fqm:
                if method_fqm in req_method_fqm:
                    self.logger.debug("Config matched for Request FQM {}".format(req_method_fqm))
                    self.common_failure(method_fqm)
                else:
                    self.logger.debug("Config not matched for Request FQM {}".format(req_method_fqm))
        else:
            self.logger.warning("config not set for apply_method_call_failure")
            # raise Exception("config not set for apply_method_call_failure")

    def increase_memory_usage(self):
        pass

    def increase_cpu_utilization(self):
        pass

    def refresh_configs(self, agent_obj):
        self.logger.info("Refreshing Configs")
        current_time_ms = time.time_ns() // 1000000

        for havoc_type in HAVOC_TYPES:
            self.logger.info("Checking havoc type: {}".format(havoc_type))

            config_list = self.netHavocConfigMap[havoc_type]
            if config_list:
                self.logger.info("Config found for havoc type: {}".format(havoc_type))
                for config in list(config_list):
                    self.logger.debug("Checking Config {} for type {}".format(id(config), config.havocType))

                    total_duration_in_ms = config.totalDurationInSec * 1000
                    self.logger.debug("total_duration_in_ms: {}".format(total_duration_in_ms))

                    start_time_ms = config.startTime
                    duration = current_time_ms - start_time_ms
                    self.logger.debug("duration: {}".format(duration))

                    # if duration >= EXPIRE_DURATION_MS:
                    if duration >= total_duration_in_ms:
                        self.logger.debug("Config {} for type {} expired, removing".format(id(config), config.havocType))
                        config_list.remove(config)

                        header_str = "NetDiagnosticMessage2.0;"
                        for key, value in config.header_dict.items():
                            header_str += key + ":" + value + ";"

                        udp.havoc_message(agent_obj, header_str)

                    else:
                        self.logger.debug("Config {} for type {} not expired, continuing".format(id(config), config.havocType))
            else:
                self.logger.warning("config not found for havoc type {}".format(havoc_type))


if __name__ == '__main__':

    # json_path = "havocprofile1.json"
    havoc_monitor = NDNetHavocMonitor()
    havoc_monitor.parse_nethavoc_config(HAVOC_PROFILES_JSON[0], HAVOC_TYPES[0])
    havoc_monitor.parse_nethavoc_config(HAVOC_PROFILES_JSON[1], HAVOC_TYPES[1])
    havoc_monitor.apply_inbound_service_delay("sample_url")
    havoc_monitor.apply_inbound_service_failure("sample_url")
    havoc_monitor.refresh_configs()
