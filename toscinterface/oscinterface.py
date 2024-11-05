import socket
from osc4py3.oscbuildparse import decode_packet, encode_packet, OSCMessage
import threading


class OscInterface:
    def __init__(self):
        self._disconnect_messages = []
        self._default_disconnect_msg = '/!DISCONNECT'
        self._host_name = socket.gethostname()
        self._host_ip = socket.gethostbyname(self._host_name)
        self._port = 8000
        self._server = None
        self._streaming = False
        self.all_responses = list()
        self.print_osc = False

    @property
    def streaming(self):
        return self._streaming

    @property
    def disconnect_messages(self):
        return self._disconnect_messages

    @property
    def default_disconnect_msg(self):
        return self._default_disconnect_msg

    @property
    def host_ip(self):
        return self._host_ip

    @property
    def host_name(self):
        return self._host_name

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_value):
        self._port = new_value

    @host_ip.setter
    def host_ip(self, new_ip):
        self._host_ip = new_ip

    def get_socket_attributes(self):
        try:
            print(f'Address Family: {self._server.family.name}\n'
                  f'Socket Type:    {self._server.type.name} \n'
                  f'Host IP:        {self._server.getsockname()[0]}\n'
                  f'Port Number:    {self._server.getsockname()[1]}')
        except AttributeError:
            raise Exception('Socket attributes are only callable while a stream is active.')
        except OSError:
            raise Exception('Socket attributes are only callable while a stream is active.')

    def start_stream(self, non_blocking=True, print_osc=True):
        if self.streaming:
            raise Exception('A stream is already running.')
        else:
            print('[STREAM STARTED]')
            self._server = self.__initialize_socket()
            self._streaming = True
            self.print_osc = print_osc
            if non_blocking:
                t = threading.Thread(target=self.__streaming_func)
                t.start()
            else:
                responses = self.__streaming_func()
                return responses

    def stop_stream(self):
        if not self.streaming:
            raise Exception('No stream is running')
        else:
            self._streaming = False
            stop_msg = OSCMessage(self._default_disconnect_msg, ',f', (1,))
            self._server.sendto(encode_packet(stop_msg), self._server.getsockname())

    def add_disconnect_msg(self, new_msg: str):
        self._disconnect_messages.append(new_msg)

    def __streaming_func(self):
        current_responses = []
        while self._streaming:
            print('Awaiting Input...')
            data, address = self._server.recvfrom(1024)
            oscmsg = decode_packet(data)
            self.all_responses.append(oscmsg)
            current_responses.append(oscmsg)
            if self.print_osc:
                print(oscmsg)
            if oscmsg.addrpattern in self._disconnect_messages or oscmsg.addrpattern == self._default_disconnect_msg:
                self._streaming = False
                print('[DISCONNECT RECEIVED] Stream stopped.')
                self._server.shutdown(socket.SHUT_RDWR)
                self._server.close()
                return current_responses
            else:
                continue

    def __initialize_socket(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server.bind((socket.gethostname(), self._port))
        return self._server
