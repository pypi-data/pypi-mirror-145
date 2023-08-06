import socket

from plogger import logger


class SocketClient:
    """Create socket and establish connect to service using tuple host+port"""

    def __init__(self,
                 host: str,
                 port: int = 0,
                 initialize: bool = False,
                 logger_enabled: bool = True,
                 connection_timeout: int = None):
        """Create and connect client to a remote host.

        :param host: Host IP
        :param port: Port
        :param logger_enabled: Enable/disable module logger
        :param initialize: Establish connection during init
        """

        self.host = host
        self.port = port
        self.logger = logger(self.__class__.__name__)
        self.logger.disabled = not logger_enabled
        self.connection_timeout = connection_timeout

        if initialize:
            try:
                self.client = self.connect(timeout=self.connection_timeout)
            except ConnectionRefusedError as err:
                self.logger.error(f'Cannot establish socket connection to {self.host}:{self.port}. {err}')
            except socket.gaierror as err:
                self.logger.error(f'Check host and port format. {self.host}:{self.port}. {err}')
            except socket.timeout as err:
                self.logger.error(f'{self.host}:{self.port} is unavailable within 7 sec. {err}')
                raise err

    def __getattr__(self, attr):
        self.logger.warning(f'No such attribute ({attr}) error. Perhaps, object is not initialized.')
        raise AttributeError(f'{self.__class__.__name__}() does not have specific attribute "{attr}"')

    def __str__(self):
        return str(self._socket_response())

    def connect(self, timeout: int = None):
        """Create connection

        :param timeout:
        :return:
        """
        return socket.create_connection((self.host, self.port), timeout=timeout)

    def is_socket_available(self,
                            port: int = 0,
                            host: str = None,
                            timeout: int = 5,
                            logger_enabled: bool = True) -> bool:
        """Check remote socket is available.

        Port 0 used by default. Used port from construct is not specified.

        :param host:
        :param port:
        :param timeout:
        :param logger_enabled:
        """

        host_ = host if host else self.host
        port_ = port if port else self.port

        try:
            with socket.create_connection((host_, port_), timeout=timeout) as sock:
                sock.settimeout(None)
                if logger_enabled:
                    self.logger.info(f'[{host_}:{port_}] is available')
                return True
        except socket.timeout:
            if logger_enabled:
                self.logger.info(f'[{host_}:{port_}] unavailable')
            return False

    def wait_socket_available(self, port: int = 0, host: str = None, timeout: int = 5):
        """Wait for a socket availability

        :param port:
        :param host:
        :param timeout:
        :return:
        """

        timer = 1
        status = self.is_socket_available(port=port, host=host, timeout=1, logger_enabled=False)

        while not status:
            status = self.is_socket_available(port=port, host=host, timeout=1, logger_enabled=False)
            timer += 1

            if timer > timeout:
                error_msg = f'The service was not started within {timeout} seconds.'
                self.logger.error(error_msg)
                raise TimeoutError(error_msg)
        return status

    def _greeting(self):
        """Works only for the first connection in all project"""
        return self._socket_response()

    def send_command(self, cmd: str = ''):
        command = self._encode_command(cmd)

        self.logger.info(f'[{self.host} -->] {cmd}')

        try:
            self.client.send(command)
            response = self._socket_response()
            return response
        except AttributeError as err:
            self.logger.error(f'[{self.host}] {err}')

    def _socket_response(self):
        """Get and decode socket response"""

        data = self.client.recv(65536).decode()
        response = data.strip().split('\n')
        self.logger.info(f'[{self.host} <--] {response}')

        return response

    def close_connection(self):
        self.client.close()

    @staticmethod
    def _encode_command(cmd):
        """Encode command to send"""

        return (cmd + '\n').encode()

    def get_sock_name(self) -> tuple:
        """Get local IP and port"""

        return self.client.getsockname()

    def get_peer_name(self) -> tuple:
        """Get remote IP and port"""
        return self.client.getpeername()
