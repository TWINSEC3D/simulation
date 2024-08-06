import tkinter as tk
import psycopg2
from tkinter import ttk
import sv_ttk
import socket
import time
import json
from datetime import datetime

class HMIClient:
    def __init__(self, host="server", port=8080, wait_time=4):
        self.host = host
        self.port = port
        self.wait_time = wait_time
        self.client_name = 'hmi'
        self.client_socket = socket.socket()

    def start(self):
        time.sleep(self.wait_time)
        self.connect_to_server()
        self.test_connection()
        self.create_hmi()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        self.log('connection', '', '')

    def test_connection(self):
        self.send_message(self.client_name)
        self.log('connection test', 'send', self.client_name)
        self.receive_message()

    def create_hmi(self):
        root = tk.Tk()
        root.title("Warehouse Data")
        root.geometry("1000x400")
        sv_ttk.set_theme("dark")
        self.set_style()
        root.after(0, self.set_style)
        self.update_table(root)

        entry_label = ttk.Label(root, text="Enter Seat ID for Outbound:", font=('Calibri', 14))
        entry_label.pack()
        entry_label.place(x=5, y=290)
        entry = ttk.Entry(root, font=("Calibri", 14), width=10)
        entry.pack()
        entry.place(x=240, y=280)

        send_button = ttk.Button(root, text="Send", command=lambda: self.process_entry(entry, root), style="TButton")
        send_button.pack()
        send_button.place(x=362, y=280)

        update_button = ttk.Button(root, text="Update", command=lambda: self.update_table(root), style="TButton")
        update_button.pack()
        update_button.place(x=900, y=280)

        root.mainloop()

    def process_entry(self, entry, root):
        input_text = entry.get()
        outbound_request = {
            'message': 'Request for Outbound',
            'id': input_text,
            'timestamp': self.current_time()
        }
        entry.delete(0, tk.END)
        try:
            if 1 <= int(input_text) <= 99999:
                self.send_message(outbound_request)
                response = self.receive_message()
                if response['message'] == 'Seat will be transported to Outbound Place.':
                    confirmation_label = ttk.Label(root, text=f'Seat {response["id"]} will be transported to Outbound Place.', font=('Calibri', 14), foreground='#2dc722')
                    confirmation_label.pack()
                    confirmation_label.place(x=5, y=330)
                    root.after(5000, lambda: self.destroy_label(confirmation_label))
            else:
                self.show_error_label(root, 'Please enter a correct Seat ID.')
        except ValueError:
            self.show_error_label(root, 'Please enter a correct Seat ID.')

    def show_error_label(self, root, message):
        error_label = ttk.Label(root, text=message, font=('Calibri', 14), foreground='#e82323')
        error_label.pack()
        error_label.place(x=5, y=330)
        root.after(5000, lambda: self.destroy_label(error_label))

    def update_table(self, root):
        db_conn = psycopg2.connect(
            database="postgres", user='postgres', password='docker', host='postgres-db', port='5432'
        )
        cursor = db_conn.cursor()
        query = "SELECT x, y, direction, seat_id, status FROM warehouse ORDER BY x, y, direction"
        cursor.execute(query)
        records = cursor.fetchall()

        for child in root.winfo_children():
            if isinstance(child, ttk.Treeview):
                child.destroy()

        tree = ttk.Treeview(root, style='Custom.Treeview')
        tree["columns"] = ("x", "y", "Direction", "Seat ID", "Status")
        tree["show"] = "headings"
        tree.heading("x", text="X", command=lambda: self.sort_column(tree, "x", False))
        tree.heading("y", text="Y", command=lambda: self.sort_column(tree, "y", False))
        tree.heading("Direction", text="Direction")
        tree.heading("Seat ID", text="Seat ID")
        tree.heading("Status", text="Status")

        for rec in records:
            rec_with_spaces = [item if item is not None else '-' for item in rec]
            tree.insert("", "end", values=rec_with_spaces)
        tree.pack()

        db_conn.close()

    def send_message(self, message):
        json_send = json.dumps(message)
        self.client_socket.send(json_send.encode())
        self.log('send', '', json_send)

    def receive_message(self):
        json_recv = self.client_socket.recv(1024).decode()
        message = json.loads(json_recv)
        self.log('recv', '', str(message))
        return message

    @staticmethod
    def sort_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (_, child) in enumerate(data):
            tree.move(child, '', index)
        tree.heading(col, command=lambda: HMIClient.sort_column(tree, col, not reverse))

    @staticmethod
    def destroy_label(label):
        label.destroy()

    @staticmethod
    def current_time():
        return str(datetime.now())

    @staticmethod
    def set_style():
        style = ttk.Style()
        style.configure("TButton", padding=4, font=("Calibri", 14, 'bold'), foreground='#7ad8fa')
        style.configure("Treeview.Heading", background="#282828", foreground="#7ad8fa", font=("Calibri", 16, "bold"))
        style.configure("Custom.Treeview", font=("Calibri", 13))

    @staticmethod
    def log(status, action, json_str):
        log = f'\n{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} {status} {action} {json_str}'
        with open("/var/log/custom.log", "a") as log_file:
            log_file.write(log)


if __name__ == '__main__':
    client = HMIClient()
    client.start()
