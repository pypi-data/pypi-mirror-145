import logging
import os
import sys
import threading
import time

from c8yrc.main import prepare_c8y_proxy, start_c8y_proxy


class TestException(Exception):

    def __init__(self, msg, original_exception):
        if original_exception:
            my_msg = '{}: {}'.format(msg, original_exception)
        else:
            my_msg = msg
        super(TestException, self).__init__(my_msg)
        self.original_exception = original_exception

class C8yThread(threading.Thread):
    def __init__(self, threadID, event, device_type, device_serial_number, user_name, user_password):
        threading.Thread.__init__(self)
        self._thread_id = threadID
        self._event = event
        self._close_down = False
        self._tenant = 't2700'
        self._script_mode = True
        self._device = f'{device_type}-{device_serial_number}'.strip()
        self._extype = 'c8y_Serial'
        self._config_name = 'Passthrough'
        self._user = user_name
        self._host = 'main.dm-zz-q.ioee10-cloud.com'
        self._password = user_password
        self._token = os.environ.get('C8Y_TOKEN')
        self._server = None  # class TCPServer

    def run(self):

        self._close_down = False
        self._server = prepare_c8y_proxy(host=self._host, device=self._device, extype=self._extype,
                                         config_name=self._config_name, tenant=self._tenant, user=self._user,
                                         password=self._password, token=None, port=20023,
                                         tfacode=None, use_pid=False, kill_instances=False, ignore_ssl_validate=False,
                                         reconnects=5,  tcp_size=32768, tcp_timeout=0, script_mode=self._script_mode,
                                         event=self._event)

        logging.info('c8y prepared')
        start_c8y_proxy(self._server, use_pid=False)
        logging.info('c8y proxy thread exit')

    def close(self):
        self._close_down = True
        if self._server:
            logging.info('closing socket')
            self._server.stop()


class C8yProxy(object):
    @staticmethod
    def get_keyword_names():
        return ['SetupC8yProxy']

    def StartC8yProxy(self, device_type, device_serial_number, rest_user_name, rest_user_password):
        event_ready = threading.Event()
        event_ready.clear()
        thread_proxy = C8yThread(1, event_ready, device_type, device_serial_number, rest_user_name, rest_user_password)
        thread_proxy.start()
        timeout = 30
        if not event_ready.wait(timeout):
            thread_proxy.close()
            raise TestException('Proxy Not Ready Exit', None)
        logging.info('proxy is ready')
        return thread_proxy


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    my_device_type = 'cb1'
    device_esn = '2102351HNDDMK2000759'
    device_address = device_esn.lower()
    device_type = my_device_type
    device_user_name = 'cbxadm'
    rest_user_name = 'service_schindler-jenkins'
    rest_user_password = '2txFLPmgE5xwWRovG7nW7e4Y94XhwOB3'
    p = C8yProxy()
    msg = f'start C8yproxy with device_type={device_type}, device_serial_number={device_address}, ' \
          f'rest_user_name={rest_user_name}, rest_user_password={rest_user_password}'
    logging.warning(msg)
    cy8_proxy_thread = p.StartC8yProxy(device_type=device_type, device_serial_number=device_address,
                                       rest_user_name=rest_user_name,
                                       rest_user_password=rest_user_password)

    logging.warning('proxy started')
    count = 0
    while count < 5:
        time.sleep(1)
        count = count + 1
    logging.warning('proxy closing')
    if cy8_proxy_thread:
        cy8_proxy_thread.close()
        cy8_proxy_thread.join()
        cy8_proxy_thread = None
    logging.warning('... done')
    time.sleep(10)
    cy8_proxy_thread = p.StartC8yProxy(device_type=device_type, device_serial_number=device_address,
                                       rest_user_name=rest_user_name,
                                       rest_user_password=rest_user_password)

    logging.warning('proxy started ')
    while count < 10:
        time.sleep(1)
        count = count + 1

    if cy8_proxy_thread:
        cy8_proxy_thread.close()
        cy8_proxy_thread.join()
        cy8_proxy_thread = None
    logging.warning('... done')

