from datetime import datetime
import socket
import _thread
import time
import json
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from models import Base, TransportUnit, Warehouse

DATABASE_URL = "postgresql+psycopg2://postgres:docker@postgres-db:5432/warehouse"


class WarehouseServer:
    def __init__(self, db_session):
        self.db_session = db_session
        self.host = '0.0.0.0'
        self.port = 8080

    def start_server(self):
        # Boot the socket
        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)

        # Test the database connection
        self.test_db_connection()

        while True:
            # Accept a new socket connection
            conn, address = server_socket.accept()
            # Test the connection
            json_recv = conn.recv(1024).decode()
            msg_recv = json.loads(json_recv)
            self.generate_log('connection test', 'recv', str(msg_recv))
            msg_send = str(msg_recv)
            json_send = json.dumps(msg_send)
            conn.send(json_send.encode())
            self.generate_log('connection test', 'send', str(msg_recv))
            # Create a new thread
            if msg_recv == 'idp_client':
                _thread.start_new_thread(self.idp_task, ('idp_client', conn, address))
            elif msg_recv == 'conveyor':
                _thread.start_new_thread(self.conveyor_task, ('conveyor', conn, address))
            elif msg_recv == 'crane':
                _thread.start_new_thread(self.crane_task, ('crane', conn, address))
            elif msg_recv == 'hmi':
                _thread.start_new_thread(self.hmi_task, ('hmi', conn, address))

    def test_db_connection(self):
        try:
            session = self.db_session()
            test_query = select(TransportUnit)
            result = session.execute(test_query).first()
            self.generate_log('database connection', '', '')
        except Exception as e:
            self.generate_log('database connection error', '', str(e))
            return

    def hmi_task(self, threadName, con, addr):
        self.generate_log('connection', '', threadName)
        session = self.db_session()

        while True:
            try:
                # Receive a message from the HMI
                json_recv = con.recv(1024).decode()
                msg_recv = json.loads(json_recv)

                # If no message is received, break
                if not msg_recv:
                    break

                self.generate_log(threadName, 'recv', str(msg_recv))

                seat_id = msg_recv['id']

                # Flag the requested seat for outbound in the database table
                stmt = update(TransportUnit).where(TransportUnit.id == seat_id).values(outbound_request=True)
                session.execute(stmt)
                session.commit()

                self.generate_log('outbound request for seat', str(seat_id), 'set in database.')

                # Send a confirmation to the HMI
                msg_send = {
                    'message': 'Seat will be transported to Outbound Place.',
                    'id': msg_recv['id']
                }
                msg_send.update({'timestamp': self.current_time()})
                json_send = json.dumps(msg_send)
                con.send(json_send.encode())
                self.generate_log(threadName, 'send', json_send)
            except Exception as e:
                self.generate_log(threadName, 'error', str(e))
                break

        # Close the connection to the HMI
        con.close()
        self.generate_log('disconnection', '', threadName)

    def idp_task(self, threadName, con, addr):
        self.generate_log('connection', '', threadName)
        session = self.db_session()

        while True:
            try:
                # Receive a message from the IDP client
                json_recv = con.recv(1024).decode()
                msg_recv = json.loads(json_recv)

                # If no message is received, break
                if not msg_recv:
                    break

                self.generate_log(threadName, 'recv', str(msg_recv))

                # Create new database table record based on the received seat data
                new_unit = TransportUnit(
                    id=msg_recv['id'], color=msg_recv['color'], type=msg_recv['type'],
                    weight=msg_recv['weight'], height=msg_recv['height'], length=msg_recv['length'],
                    width=msg_recv['width'], current_loc=msg_recv['current_loc'],
                    outbound_request=msg_recv['outbound_request']
                )
                session.add(new_unit)
                session.commit()
                log_str = 'data of seat ' + msg_recv['id'] + ' saved in database.'
                self.generate_log(log_str, '', '')

                # Send a confirmation to the IDP client
                msg_send = {
                    'message': 'ID saved in DB',
                    'id': msg_recv['id'],
                }
                msg_send.update({'timestamp': self.current_time()})
                json_send = json.dumps(msg_send)
                con.send(json_send.encode())
                self.generate_log(threadName, 'send', json_send)
            except Exception as e:
                self.generate_log(threadName, 'error', str(e))
                break

        # Close the connection to the IDP client
        con.close()
        self.generate_log('disconnection', '', threadName)

    def conveyor_task(self, threadName, con, addr):
        self.generate_log('connection', '', threadName)
        session = self.db_session()

        while True:
            try:
                # Receive a message from the conveyor
                json_recv = con.recv(1024).decode()
                msg_recv = json.loads(json_recv)

                # If no message is received, break
                if not msg_recv:
                    break

                self.generate_log(threadName, 'recv', str(msg_recv))

                # Check if the received message is a request message
                if msg_recv['message'] == 'Request for transport':
                    # Search database for seats waiting at the identification point that need to be transported to the inbound place
                    stmt = select(TransportUnit.id).where(TransportUnit.current_loc == 'IDP')
                    db_record = session.execute(stmt).first()

                    # Declare a 'no operation' message if there are no seats at the identification point
                    if not db_record:
                        msg_send = {'message': 'No operation'}
                    # Declare a transport order if there is a seat waiting at the identification point
                    else:
                        seat_id = db_record[0]
                        msg_send = {
                            'message': 'Move to',
                            'from': 'IDP',
                            'to': 'Inbound_place',
                            'id': seat_id,
                        }
                # If the message is not a request, it is the confirmation of a successful transport
                else:
                    seat_id = str(msg_recv['id'])

                    # Update the database record by setting the current location of the seat to 'inbound_place'
                    stmt = update(TransportUnit).where(TransportUnit.id == seat_id).values(current_loc='Inbound_place')
                    session.execute(stmt)
                    session.commit()
                    log_str = "new location 'inbound place' of seat " + msg_recv['id'] + " saved in database."
                    self.generate_log(log_str, '', '')

                    # Declare a confirmation message
                    msg_send = {
                        'message': 'Acknowledge',
                        'id': seat_id
                    }

                # Send a message to the conveyor
                msg_send.update({'timestamp': self.current_time()})
                json_send = json.dumps(msg_send)
                con.send(json_send.encode())
                self.generate_log(threadName, 'send', str(json_send))
            except Exception as e:
                self.generate_log(threadName, 'error', str(e))
                break

        # Close the connection to the conveyor
        con.close()
        self.generate_log('disconnection', '', threadName)

    def crane_task(self, threadName, con, addr):
        self.generate_log('connection', '', threadName)
        session = self.db_session()

        while True:
            try:
                # Receive a message from the crane
                json_recv = con.recv(1024).decode()
                msg_recv = json.loads(json_recv)

                # If no message is received, break
                if not msg_recv:
                    break

                self.generate_log(threadName, 'recv', str(msg_recv))

                # Check if the received message is a request message
                if msg_recv['message'] == 'Request for transport':
                    # Search the database for seats waiting for outbound
                    query_outbound = """
                        SELECT tu.id, wh.y, wh.x, wh.direction 
                        FROM transport_units tu 
                        LEFT JOIN warehouse wh ON tu.id = wh.seat_id 
                        WHERE tu.current_loc = 'WH' AND tu.outbound_request = true
                    """
                    db_record_outbound = session.execute(query_outbound).first()

                    if db_record_outbound:
                        seat_id, y, x, direction = db_record_outbound
                        # Check for the bin of outbound seat
                        if direction:
                            # Declare an outbound order
                            msg_send = {
                                'message': 'Move to',
                                'from': 'Warehouse',
                                'to': 'Outbound_place',
                                'y': y,
                                'x': x,
                                'direction': direction,
                                'id': seat_id
                            }
                        # If the bin of outbound seat cannot be found, save error to the database and declare a 'no operation' message
                        else:
                            self.generate_log('unknown location', '', str(seat_id))
                            stmt = update(TransportUnit).where(TransportUnit.id == seat_id).values(current_loc='WH bin not found')
                            session.execute(stmt)
                            session.commit()
                            log_str = "new location 'WH bin not found' of seat " + str(seat_id) + " saved in database."
                            self.generate_log(log_str, '', '')
                            msg_send = {'message': 'No operation'}
                    # If there is no seat waiting for outbound, check for seats waiting for inbound
                    else:
                        # Search database for seats waiting for inbound
                        stmt = select(TransportUnit.id).where(TransportUnit.current_loc == 'Inbound_place')
                        db_record_inbound = session.execute(stmt).first()

                        if db_record_inbound:
                            seat_id = db_record_inbound[0]
                            # Search database for an empty bin
                            stmt = select(Warehouse.y, Warehouse.x, Warehouse.direction).where(Warehouse.seat_id == None).where(Warehouse.status == None).order_by(Warehouse.y, Warehouse.x)
                            db_record_bin = session.execute(stmt).first()

                            y, x, direction = db_record_bin
                            # Declare an inbound order
                            msg_send = {
                                'message': 'Move to',
                                'from': 'Inbound_place',
                                'to': 'Warehouse',
                                'y': y,
                                'x': x,
                                'direction': direction,
                                'id': seat_id
                            }
                        # If there is no seat waiting for inbound, declare a 'no operation' message
                        else:
                            msg_send = {'message': 'No operation'}

                # Check if the received message is a transport confirmation
                elif msg_recv['message'] == 'Moved':
                    id = str(msg_recv['id'])
                    seat_y = msg_recv['y']
                    seat_x = msg_recv['x']
                    seat_direction = str(msg_recv['direction'])

                    # Check if the confirmation message concerns an outbound
                    if msg_recv['from'] == 'Warehouse' and msg_recv['to'] == 'Outbound_place':
                        # Update current location of the seat to 'outbound_place' and flag the bin as empty
                        stmt1 = update(TransportUnit).where(TransportUnit.id == id).values(outbound_request=False, current_loc='Outbound_place')
                        stmt2 = update(Warehouse).where(Warehouse.y == seat_y).where(Warehouse.x == seat_x).where(Warehouse.direction == seat_direction).values(seat_id=None)
                        session.execute(stmt1)
                        session.execute(stmt2)
                        log_str = "new location 'outbound place' of seat " + id + " saved in database."
                        log_str_2 = 'bin y: ' + str(seat_y) + ', x: ' + str(seat_x) + ', direction: ' + seat_direction + ' flagged as empty.'
                    # Check if the confirmation message concerns an inbound
                    elif msg_recv['from'] == 'Inbound_place' and msg_recv['to'] == 'Warehouse':
                        # Update the current location of the seat to 'warehouse' and flag the bin as occupied
                        stmt1 = update(TransportUnit).where(TransportUnit.id == id).values(current_loc='WH')
                        stmt2 = update(Warehouse).where(Warehouse.y == seat_y).where(Warehouse.x == seat_x).where(Warehouse.direction == seat_direction).values(seat_id=id)
                        session.execute(stmt1)
                        session.execute(stmt2)
                        log_str = "new location 'warehouse' of seat " + str(id) + " saved in database."
                        log_str_2 = 'bin y: ' + str(seat_y) + ', x: ' + str(seat_x) + ', direction: ' + seat_direction + ' flagged as occupied.'

                    # Save changes to the database
                    session.commit()
                    self.generate_log(log_str, '', '')
                    self.generate_log(log_str_2, '', '')

                    # Declare a confirmation message
                    msg_send = {
                        'message': 'Acknowledge',
                        'id': id
                    }

                # Check if the received message is an empty error message
                elif msg_recv['message'] == 'Empty':
                    self.generate_log('error', 'recv', str(msg_recv))
                    seat_id = str(msg_recv['id'])
                    seat_y = msg_recv['y']
                    seat_x = msg_recv['x']
                    seat_direction = str(msg_recv['direction'])

                    # Save the error in the database
                    stmt1 = update(TransportUnit).where(TransportUnit.id == seat_id).values(current_loc='WH error empty')
                    stmt2 = update(Warehouse).where(Warehouse.seat_id == seat_id).values(status='error empty')
                    session.execute(stmt1)
                    session.execute(stmt2)
                    session.commit()

                    log_str = "new location 'WH error empty' of seat " + seat_id + " saved in database."
                    log_str_2 = "status of bin of seat " + seat_id + " set to 'error empty'."
                    self.generate_log(log_str, '', '')
                    self.generate_log(log_str_2, '', '')

                    # Declare a confirmation message
                    msg_send = {
                        'message': 'Acknowledge',
                        'id': seat_id
                    }

                # Check if the received message is an occupied error message
                elif msg_recv['message'] == 'Occupied':
                    self.generate_log('error', 'recv', str(msg_recv))
                    id = str(msg_recv['id'])
                    seat_y = msg_recv['y']
                    seat_x = msg_recv['x']
                    seat_direction = str(msg_recv['direction'])

                    # Save the error in the database
                    stmt = update(Warehouse).where(Warehouse.y == seat_y).where(Warehouse.x == seat_x).where(Warehouse.direction == seat_direction).values(status='error occupied')
                    session.execute(stmt)
                    session.commit()

                    log_str = "status of bin y: " + str(seat_y) + ", x: " + str(seat_x) + ", direction: " + seat_direction + " set to 'error occupied'."
                    self.generate_log(log_str, '', '')

                    # Search the database for another empty bin
                    stmt = select(Warehouse.y, Warehouse.x, Warehouse.direction).where(Warehouse.seat_id == None).where(Warehouse.status == None).order_by(Warehouse.y, Warehouse.x)
                    db_record_bin = session.execute(stmt).first()

                    y, x, direction = db_record_bin
                    # Declare a transport message with new bin coordinates
                    msg_send = {
                        'message': 'Move to',
                        'from': 'Inbound_place',
                        'to': 'Warehouse',
                        'y': y,
                        'x': x,
                        'direction': direction,
                        'id': id
                    }

                # Send a message to the crane
                msg_send.update({'timestamp': self.current_time()})
                json_send = json.dumps(msg_send)
                con.send(json_send.encode())
                self.generate_log(threadName, 'send', str(json_send))
            except Exception as e:
                self.generate_log(threadName, 'error', str(e))
                break

        # Close the connection to the crane
        con.close()
        self.generate_log('disconnection', '', threadName)

    @staticmethod
    def current_time():
        return str(datetime.now())

    @staticmethod
    def generate_log(status, action, json_str):
        log = '\n' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ' ' + status + ' ' + action + ' ' + json_str
        with open("/var/log/server.log", "a") as log_file:
            log_file.write(log)


def create_db_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session()


if __name__ == '__main__':
    db_session = create_db_session()
    server = WarehouseServer(db_session)
    server.start_server()
