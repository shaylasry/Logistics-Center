import atexit
import sqlite3
from Clinic import Clinic
from Clinics import Clinics
from Logistic import Logistic
from Logistics import Logistics
from Supplier import Supplier
from Suppliers import Suppliers
from Vaccine import Vaccine


from Vaccines import Vaccines


class Repository:
    vaccinesCounter = 1
    def __init__(self):
        self._conn = sqlite3.connect("db_tested.db")
        self.vaccines = Vaccines(self._conn)
        self.logistics = Logistics(self._conn)
        self.clinics = Clinics(self._conn)
        self.suppliers = Suppliers(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def delete_tables(self):
        self._conn.executescript("""DROP TABLE IF EXISTS vaccines;
        DROP TABLE IF EXISTS suppliers;
        DROP TABLE IF EXISTS clinics;
        DROP TABLE IF EXISTS logistics;""")

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE vaccines(
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            supplier INTEGER REFERENCES suppliers(id),
            quantity INTEGER NOT NULL);
        CREATE TABLE suppliers(
            id INTEGER PRIMARY KEY, 
            name STRING NOT NULL,
            logistic INTEGER REFERENCES logistics(id));
        CREATE TABLE clinics( 
            id INTEGER PRIMARY KEY, 
            location STRING NOT NULL,
            demand INTEGER NOT NULL,
            logistic INTEGER REFERENCES logistics(id));
        CREATE TABLE logistics( 
            id INTEGER PRIMARY KEY, 
            name STRING NOT NULL,
            count_sent INTEGER NOT NULL,
            count_received INTEGER NOT NULL);
    """)




    def getInventory(self):
        to_sum = self.vaccines.get_quantity()
        final_sum = 0
        for i in range(0, len(to_sum)):
            final_sum = final_sum + to_sum[i].quantity
        return final_sum

    def getTotalDemand(self):
        to_sum = self.clinics.get_demand()
        final_sum = 0
        for i in range(0, len(to_sum)):
            final_sum = final_sum + to_sum[i].demand
        return final_sum
    def getTotalReceived(self):
        to_sum = self.logistics.get_count_received()
        final_sum = 0
        for i in range(0, len(to_sum)):
            final_sum = final_sum + to_sum[i].count_received
        return final_sum

    def getTotalSent(self):
        to_sum = self.logistics.get_count_sent()
        final_sum = 0
        for i in range(0, len(to_sum)):
            final_sum = final_sum + to_sum[i].count_sent
        return final_sum


repo = Repository()

atexit.register(repo.close)
