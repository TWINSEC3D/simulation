from datetime import datetime
import socket
import time
import json
import random

class IDPClient:
    def __init__(self, host="server", port=8080, wait_time=1):
        self.host = host
        self.port = port
        self.wait_time = wait_time
        self.client_name = 'idp_client'
        self.id = 1
        self.client_socket = socket.socket()

    def start(self):
        time.sleep(self.wait_time)
        self.connect_to_server()
        self.test_connection()

        if self.receive_message() == self.client_name:
            while True:
                self.send_seat_data()
                self.receive_confirmation()
                self.id += 1
                time.sleep(90)

        self.disconnect()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        self.log('connection', '', '')

    def test_connection(self):
        self.send_message(self.client_name)
        self.log('connection test', 'send', self.client_name)
        self.receive_message()

    def send_seat_data(self):
        seat_data = self.generate_seat_data(str(self.id).zfill(5))
        self.send_message(seat_data)
        self.log('seat arrival', 'send', json.dumps(seat_data))

    def receive_confirmation(self):
        message = self.receive_message()
        self.log('response', 'recv', str(message))

    def disconnect(self):
        self.client_socket.close()
        self.log('disconnection', '', '')

    def send_message(self, message):
        json_send = json.dumps(message)
        pre = time.time()
        self.client_socket.send(json_send.encode())
        post = time.time()
        response_time = post - pre
        status = self.response_time_status(response_time)
        self.log(status, str(response_time), '')

    def receive_message(self):
        json_recv = self.client_socket.recv(1024).decode()
        message = json.loads(json_recv)
        return message

    def generate_seat_data(self, id_str):
        colors = ['black', 'brown', 'beige']
        types = ['front', 'back']
        weights = [25000, 27000]
        heights = [1000, 1050, 1100]
        lengths = [550, 600]
        widths = [500, 550]

        seat_data = {
            'id': id_str,
            'color': random.choice(colors),
            'type': random.choice(types),
            'weight': random.choice(weights),
            'height': random.choice(heights),
            'length': random.choice(lengths),
            'width': random.choice(widths),
            'current_loc': 'IDP',
            'outbound_request': 'false'
        }
        seat_data.update({'timestamp': self.current_time()})
        return seat_data

    @staticmethod
    def current_time():
        return str(datetime.now())[:-7]

    @staticmethod
    def log(status, action, json_str):
        log = f'\n{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} {status} {action} {json_str}'
        with open("/var/log/custom.log", "a") as log_file:
            log_file.write(log)

    @staticmethod
    def response_time_status(response_time):
        return 'response time ok' if response_time <= 1 else 'slow response'


if __name__ == '__main__':
    client = IDPClient()
    client.start()
