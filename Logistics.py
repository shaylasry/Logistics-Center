from Logistic import Logistic
class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
               INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find_logistic_by_clinic(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT  * FROM logistics WHERE id = ?
        """, [clinic_id])

        return Logistic(*c.fetchone())


    def update_count_sent(self, set_values, id_update):
        c = self._conn.cursor()
        c.execute("""
                      UPDATE logistics SET count_sent = (?) WHERE id = (?)
                  """, [set_values, id_update])

    def find_logistic_by_supplier(self, supplier_logistic):
        c = self._conn.cursor()
        c.execute("""
               SELECT  * FROM logistics WHERE id = ?
           """, [supplier_logistic])
        return Logistic(*c.fetchone())

    def update_count_received(self, set_values, logistic_id):
        c = self._conn.cursor()
        c.execute("""
                   UPDATE logistics SET count_received = (?) WHERE id = (?)
               """, [set_values, logistic_id])

    def get_count_received(self):
        c = self._conn.cursor()
        all = c.execute("""
               SELECT * FROM logistics
           """).fetchall()
        return [Logistic(*row) for row in all]

    def get_count_sent(self):
        c = self._conn.cursor()
        all = c.execute("""
               SELECT * FROM logistics
           """).fetchall()
        return [Logistic(*row) for row in all]
