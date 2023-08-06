import uuid
import os
import socket

import sys
import threading
import json
from .udp_message import create_start_transaction_message, create_end_transaction_message
from .udp_message import create_method_entry_message, create_method_exit_message
from .udp_message import create_havoc_message
from .udp_message import create_init_message
import time


#from .udp_message import create_transaction_encode_http_message

udp_connection = None

class UDPConnection(object):
    def __init__(self):

        if 'CAV_APP_AGENT_PROXYIP' in os.environ:
            self.cav_proxy_ip = os.environ['CAV_APP_AGENT_PROXYIP']
        else:
            self.cav_proxy_ip = "127.0.0.1"

        if 'CAV_APP_AGENT_PROXYPORT' in os.environ:
            self.cav_proxy_port = int(os.environ['CAV_APP_AGENT_PROXYPORT'])

        else:
            self.cav_proxy_port = 10000

        self.server_address_port = (self.cav_proxy_ip, self.cav_proxy_port)

        # Create a UDP socket at client side
        try:

            self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            print("Server, Port", self.server_address_port)

            havoc_thread = threading.Thread(target=incoming_message_processor, name="havoc_thread",
                                            args=(self.UDPClientSocket,), daemon=True)
            havoc_thread.start()

        except:
            print("Unable to create UDP Connection")

    def send(self, message, tx_type="non_start_fp"):

        # Send to server using created UDP socket
        try:
            print("Sending", tx_type)
            self.UDPClientSocket.sendto(message, self.server_address_port)

            """
            if tx_type == "start_fp":
                print("TX type : start fp")

                havoc_thread = threading.Thread(target=incoming_message_processor, name="havoc_thread",
                                                args=(self.UDPClientSocket,), daemon=True)
                havoc_thread.start()
            """

        except:
            print("Unable to send UDP packet")


def incoming_message_processor(udp_socket):
    print("New thread started: incoming message")

    from pythonagent.agent.probes.havoc.havoc_manager import NDNetHavocMonitor  # Don't shift to top, it will cause circular import
    havoc_monitor = NDNetHavocMonitor.get_instance()
    print("udp.py havoc id ", id(havoc_monitor))
    while True:
        buffer_size = 1024

        #time.sleep(1)
        print("Going to call recv from api")

        data, address = udp_socket.recvfrom(buffer_size)
        print("\n\nincoming received message = ", data, "\n\n")

        output = str(data)

        try:
            # WITH NEWLINE

            output = output[2:-1]  # Remove b' from beginning and ' from end
            split_arr = output.split("\\n")

            header = split_arr[0]
            body = split_arr[1]

            body = body.replace("-", ":")

            header = header[:-1]  # Trim ; from end
            header_dict = {}

            header_split = header.split(";")

            count = 0
            for element in header_split:
                if count == 0:
                    count += 1
                    continue  # Ignore first value: NetDiagnosticMessage2.0
                else:
                    element_split = element.split(":")
                    key = element_split[0].strip()
                    value = element_split[1].strip()
                    header_dict[key] = value
                    count += 1

            havoc_monitor.parse_nethavoc_config(body, header_dict)

            # WITHOUT NEWLINE

            """
            output = output[26:]  # Trim b'NetDiagnosticMessage2.0; from start
            output = output[:-1]  # Trim ; from end

            output_split = output.split(";")

            header = output_split[1:-2]  # Remove first and last 2 (empty) elements
            body = output_split[-2]  # Second Last element

            header_dict = {}

            for element in header:
                element_split = element.split(":")
                key = element_split[0].strip()
                value = element_split[1].strip()
                header_dict[key] = value

            body = body[7:]  # Trim config: from beginning
            body = body.replace("-", ":")
            
            havoc_monitor.parse_nethavoc_config(body, header_dict)
            """

        except Exception as e:
            print("Unable to parse config: ", e)
            pass


def generate_bt():
    id = uuid.uuid4()
    id_int = id.int
    return id_int


def sdk_init(agent_obj):
    agent_obj.udp_connection = UDPConnection()
    context = agent_obj.get_transaction_context()
    print("transaction context dictionary inside sdk init in udp.py", context.function_name)
    message = create_init_message(context)
    print("first message to be sent to proxy", message)
    agent_obj.udp_connection.send(message)
    return udp_connection


def sdk_free(agent_obj):
    pass


def method_entry(agent_obj, bt, method, query_string, url_parameter):
    context = agent_obj.get_transaction_context()
    message = create_method_entry_message(context, bt, method, query_string, url_parameter)
    print("method_entry ", message)
    agent_obj.udp_connection.send(message)


def method_exit(agent_obj, bt, method, backend_header, status, duration):
    context = agent_obj.get_transaction_context()
    #message = create_method_exit_message(context, bt, method)
    message = create_method_exit_message(context, bt, method, backend_header, status, duration)
    print("method_exit: status, duration, message", status, duration, message)
    agent_obj.udp_connection.send(message)


def start_business_transaction(agent_obj, bt_name, correlation_header):
    if os.environ['nd_init_done'] == '0':
        agent_obj.sdk_init()

    context = agent_obj.get_transaction_context()
    # message = udp_message.create_start_transaction_message(context, bt_name, correlation_header)
    message = create_start_transaction_message(context, bt_name, correlation_header)
    print("start_business_transaction ", message)
    #print("length:", len(message))
    agent_obj.udp_connection.send(message, "start_fp")

    bt = generate_bt()

    agent_obj.active_bts.add(bt)
    agent_obj.set_current_bt(bt)

    return bt


def end_business_transaction(agent_obj, bt):
    status_code = agent_obj.get_current_status_code()
    context = agent_obj.get_transaction_context()
    # message = udp_message.create_end_transaction_message(context, bt, status_code)
    message = create_end_transaction_message(context, bt, status_code)
    # print("print end_business_transaction: status_code, message ", status_code, message)
    agent_obj.logger.debug("status_code {}, message {}".format(status_code, message))
    # agent_obj.logger.info("status_code {}, message {}".format(status_code, message))
    # agent_obj.logger.warning("status_code {}, message {}".format(status_code, message))
    # agent_obj.logger.error("status_code {}, message {}".format(status_code, message))
    # agent_obj.logger.critical("status_code {}, message {}".format(status_code, message))

    agent_obj.udp_connection.send(message)

    rc = 0  # DUMMY VALUE FOR SUCCESS

    agent_obj.reset_transaction_context()

    # agent_obj.unset_current_bt()
    # agent_obj.unset_current_status_code()
    # agent_obj.active_bts.discard(bt)

    return rc


def store_business_transaction(agent_obj, bt, unique_bt_id):
    pass


def db_call_begin(agent_obj, bt, db_host, db_query):
    pass


def db_call_end(agent_obj, bt, ip_handle):
    pass


def http_call_begin(agent_obj, bt, http_host, url):
    #context = agent_obj.get_transaction_context()
    #message = create_transaction_encode_http_message(context, bt, http_host, url)
    #agent_obj.udp_connection.send(message)
    handle = 1  # DUMMY NON ZERO VALUE
    return handle


def http_call_end(agent_obj, bt, ip_handle):
    pass


def havoc_message(agent_obj, havoc_header):
    context = agent_obj.get_transaction_context()
    message = create_havoc_message(context, havoc_header)
    print("havoc_message: ", message)
    agent_obj.udp_connection.send(message)
