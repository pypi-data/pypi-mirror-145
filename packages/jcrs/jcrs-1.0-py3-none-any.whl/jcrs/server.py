import abc
import argparse
import logging
import signal
import socket
import sys
import threading
import time
from signal import SIGHUP, SIGINT, SIGQUIT, SIGTERM
from threading import Thread


def main():
    parser = argparse.ArgumentParser(description='JenCat Relay Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind server on')
    parser.add_argument('--port', type=int, default=4200, help='Port to bind server on')
    parser.add_argument('--yes', action='store_true', required=True, help='Just to make sure you have read the help :)')
    args = parser.parse_args()
    yes = args.yes
    if not yes:
        raise RuntimeError("Make sure you read help!")
    srv = JCServer(host=args.host, port=args.port)
    srv.start()
    srv.join()


class UseLogging:
    LOG_LEVEL = logging.DEBUG

    def __new__(cls, target):
        def init_logger(self2):
            self2.logger = logging.getLogger(self2.__class__.__qualname__)
            self2.logger.setLevel(self2.LOG_LEVEL)
            ch = logging.StreamHandler()
            ch.setLevel(self2.LOG_LEVEL)
            formatter = logging.Formatter("[%(asctime)s][%(module)s][%(threadName)25s][%(levelname)10s]: %(message)s")
            ch.setFormatter(formatter)
            self2.logger.addHandler(ch)

        target_init = target.__init__

        if not hasattr(target, 'LOG_LEVEL'):
            target.LOG_LEVEL = UseLogging.LOG_LEVEL

        def __new_init__(_self, *_args, **_kwargs):
            target_init(_self, *_args, **_kwargs)
            _self.init_logger()

        target.init_logger = init_logger
        target.__init__ = __new_init__
        return target


class SmartThread(object):
    LOG_LEVEL = logging.DEBUG

    def __init__(self, server, *args, **kwargs):
        self.server = server
        self.thread = Thread(
            target=self.smart_thread,
            name=self.__class__.__qualname__,
            args=args,
            kwargs=kwargs,
            daemon=True
        )
        self.should_run = False
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.logger.setLevel(self.LOG_LEVEL)
        ch = logging.StreamHandler()
        ch.setLevel(self.LOG_LEVEL)
        formatter = logging.Formatter("[%(asctime)s][%(module)s][%(threadName)25s][%(levelname)10s]: %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def start(self):
        self.should_run = True
        self.thread.start()

    def stop(self):
        self.should_run = False

    def is_alive(self):
        return self.thread.is_alive()

    def join(self, *args, **kwargs):
        self.thread.join(*args, **kwargs)

    def smart_thread(self, *args, **kwargs):
        try:
            self.pre_exec(*args, **kwargs)
            while not self.server.exit_event.is_set() and self.should_run:
                self.loop(*args, **kwargs)
        except Exception as e:
            print(e)
            raise e
        finally:
            try:
                self.post_exec(*args, **kwargs)
            except:  # noqa
                pass

    @abc.abstractmethod
    def loop(self, *args, **kwargs):
        pass

    def pre_exec(self, *args, **kwargs):
        pass

    def post_exec(self, *args, **kwargs):
        pass


class Worker(SmartThread):

    def __init__(self, server, conn, addr):
        super(Worker, self).__init__(server)
        self.conn = conn
        self.addr = addr

    def pre_exec(self, *args, **kwargs):
        self.conn.setblocking(True)

    def loop(self):
        """
        Worker for a single client connection
        :return:
        """
        try:
            data = self.conn.recv(self.server.recv_buffer)
            if data == b'':
                self.logger.debug(f' > client {self.addr} disconnecting...')
                self.conn.close()
                return self.stop()
            self.server.broadcast(str(self.addr), data)
        except BlockingIOError:
            time.sleep(sys.getswitchinterval())
        except Exception:  # noqa
            self.conn.close()
            return self.stop()

    def post_exec(self, *args, **kwargs):
        self.conn.close()


class GarbageCollector(SmartThread):

    def pre_exec(self, *args, **kwargs):
        self.logger.debug(f'@GarbageCollector started')

    def loop(self):
        """
        Threaded function for removing disconnected clients' data from memory
        :return:
        """
        time.sleep(sys.getswitchinterval())
        if len(self.server.threads) > 0:
            for k, t in self.server.threads.copy().items():
                if not t.is_alive():
                    time.sleep(sys.getswitchinterval())
                    if not t.is_alive():
                        self.logger.debug(f'@GarbageCollector: Reaper deleted thread with key {k}')
                        del self.server.threads[k]
                        del self.server.clients[k]
                        break


@UseLogging
class JCServer:

    def __init__(self, host='0.0.0.0', port=8842, recv_buffer=128, backlog=1024):
        super(JCServer, self).__init__()
        self.exit_event = threading.Event()
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.backlog = backlog
        self.lock = threading.Lock()
        self.should_run = False
        self.threads = dict()
        self.clients = dict()
        self.reaper = None
        self.sock = None
        self.accept_thread = Thread(target=self.accept, daemon=False)
        self.reaper = GarbageCollector(self)

    def __signal_handler(self, sig, _):
        """
        Signal handler for exitting
        :param sig:
        :param _:
        :return:
        """
        self.logger.debug(f'>> Signal handler -> {signal.strsignal(sig)}')
        self.exit_event.set()
        self.should_run = False

    def __register_signal_handler(self):
        for sig in SIGTERM, SIGINT, SIGQUIT, SIGHUP:
            signal.signal(sig, self.__signal_handler)

    def start(self):
        """
        Start the server
        :return:
        """
        self.should_run = True
        self.__register_signal_handler()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # >>> Try reuse addr ----------------------------------------------------
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception:  # noqa
            pass
        # >>> Try reuse addr ----------------------------------------------------
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except Exception:  # noqa
            pass
        # -----------------------------------------------------------------------
        # Start server
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)
        self.sock.setblocking(False)
        self.accept_thread.start()
        self.reaper.start()
        self.logger.info(f"@JCServer: listening on {self.host}:{self.port} ...")

    def accept(self):
        """
        Accept connection
        :return:
        """
        _flag = True
        while not self.exit_event.is_set():
            if _flag:
                self.logger.debug('@JCServer: Waiting for connection...')
                _flag = False
            try:
                conn, addr = self.sock.accept()
            except BlockingIOError:
                time.sleep(sys.getswitchinterval())
                continue
            else:
                _flag = True
                with self.lock:
                    self.clients[f'{addr}'] = (conn, addr)
                    self.logger.debug(f"@JCServer: Accepted connection from {repr(addr)}, starting async")
                    self.threads[f'{addr}'] = Worker(self, conn, addr)
                    self.threads[f'{addr}'].start()

    def broadcast(self, _from, msg):
        """
        Broadcast message to all connected clients
        :param _from:
        :param msg:
        :return:
        """
        with self.lock:
            items = [*self.clients.items()]
            for cid, (conn, addr) in items:
                try:
                    conn.sendall(msg)
                except Exception:  # noqa
                    pass

    def join(self, timeout=None):
        """
        Join the server threads
        :param timeout:
        :return:
        """
        self.accept_thread.join(timeout)
        self.reaper.join()
