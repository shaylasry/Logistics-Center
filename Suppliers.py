from Supplier import Supplier
class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.logistic])



    def find_supplier_by_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
               SELECT  * FROM suppliers WHERE name = ?
           """, [supplier_name])
        return Supplier(*c.fetchone())