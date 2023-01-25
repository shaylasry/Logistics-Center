from Clinic import Clinic
class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
               INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
           """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])



    def find_clinic_by_location(self, location_p):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE location = ?
        """, [location_p])
        return Clinic(*c.fetchone())

    def update_demand(self, set_values, location_p):
        c = self._conn.cursor()
        c.execute("""
                   UPDATE clinics SET demand = (?) WHERE location = (?)
               """, [set_values, location_p])

    def get_demand(self):
        c = self._conn.cursor()
        all = c.execute("""
               SELECT * FROM clinics
           """).fetchall()
        return [Clinic(*row) for row in all]