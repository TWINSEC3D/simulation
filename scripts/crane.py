import socket
import time
from datetime import datetime
import json
import random

class CraneClient:
    def __init__(self, host="server", port=8080, wait_time=3):
        self.host = host
        self.port = port
        self.wait_time = wait_time
        self.client_name = 'crane'
        self.client_socket = socket.socket()

    def start(self):
        time.sleep(self.wait_time)
        self.connect_to_server()
        self.test_connection()
        self.handle_requests()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        self.log('connection', '', '')

    def test_connection(self):
        self.send_message(self.client_name)
        self.log('connection test', 'send', self.client_name)
        self.receive_message()

    def handle_requests(self):
        request = {'message': 'Request for transport', 'timestamp': self.current_time()}
        msg_send = request
        status = 'request'

        while True:
            self.send_message(msg_send)
            response = self.receive_message()

            if response['message'] == 'Move to':
                msg_send, status = self.handle_move_to(response)
                waiting_time = 30
            elif response['message'] == 'No operation':
                request['timestamp'] = self.current_time()
                msg_send = request
                status = 'request'
                waiting_time = 10
            elif response['message'] == 'Acknowledge':
                request['timestamp'] = self.current_time()
                msg_send = request
                status = 'request'
                waiting_time = 0

            time.sleep(waiting_time)

        self.disconnect()

    def handle_move_to(self, response):
        origin = response['from']
        destination = response['to']
        id = response['id']
        y = response['y']
        x = response['x']
        direction = response['direction']
        
        random_number = random.randint(1, 20)
        
        if random_number <= 1 and origin == 'Inbound_place' and destination == 'Warehouse':
            msg_send = {'message': 'Occupied', 'id': id, 'y': y, 'x': x, 'direction': direction}
            status = 'bin occupied'
        elif random_number <= 1 and origin == 'Warehouse' and destination == 'Outbound_place':
            msg_send = {'message': 'Empty', 'id': id, 'y': y, 'x': x, 'direction': direction}
            status = 'bin empty'
        else:
            msg_send = {
                'message': 'Moved', 'from': origin, 'to': destination, 'id': id, 'y': y, 'x': x, 'direction': direction
            }
            status = 'transport success'

        msg_send.update({'timestamp': self.current_time()})
        return msg_send, status

    def disconnect(self):
        self.client_socket.close()
        self.log('disconnection', '', '')

    def send_message(self, message):
        json_send = json.dumps(message)
        pre = time.time()
        self.client_socket.send(json_send.encode())
        self.log('send', '', json_send)
        post = time.time()
        response_time = post - pre
        status = self.response_time_status(response_time)
        self.log(status, str(response_time), '')

    def receive_message(self):
        json_recv = self.client_socket.recv(1024).decode()
        message = json.loads(json_recv)
        self.log('recv', '', str(message))
        return message

    @staticmethod
    def current_time():
        return str(datetime.now())

    @staticmethod
    def log(status, action, json_str):
        log = f'\n{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} {status} {action} {json_str}'
        with open("/var/log/crane.log", "a") as log_file:
            log_file.write(log)

    @staticmethod
    def response_time_status(response_time):
        return 'response time ok' if response_time <= 1 else 'slow response'


if __name__ == '__main__':
    client = CraneClient()
    client.start()
