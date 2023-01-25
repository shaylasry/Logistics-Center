from Vaccine import Vaccine
class Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
               SELECT * FROM vaccines
           """).fetchall()
        return [Vaccine(*row) for row in all]

    def update_quantity(self, set_values, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
                      UPDATE vaccines SET quantity = (?) WHERE id = (?)
                  """, [set_values, vaccine_id])

    def delete_vaccine(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""DELETE FROM vaccines WHERE id =(?)""", [vaccine_id])

    def get_quantity(self):
        c = self._conn.cursor()
        all = c.execute("""
               SELECT * FROM vaccines
           """).fetchall()
        return [Vaccine(*row) for row in all]