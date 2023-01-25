import sys


from datetime import datetime

from Clinic import Clinic
from Logistic import Logistic
from Repository import repo
from Supplier import Supplier
from Vaccine import Vaccine
from Clinics import Clinics
from Logistics import Logistics
from Suppliers import Suppliers
from Vaccines import Vaccines



def main(args):
    repo.delete_tables()
    repo.create_tables()
    populate_tables(sys.argv[1])
    output(sys.argv[3], sys.argv[2])





def populate_tables(config_file_name):
    with open(config_file_name) as config_file:
        type_read_count = config_file.readline().split(',')

        # read the vaccines
        for i in range(0, int(type_read_count[0])):
            data_line = config_file.readline().split(',')
            vac_id = int(data_line[0])
            vac_supplier_id = int(data_line[2])
            vac_quantity = int(data_line[3])

            vac_date = data_line[1]
            conv_vac_date = datetime.strptime(vac_date, '%Y-%m-%d')

            # create a vaccine in the table
            new_vac = Vaccine(vac_id, conv_vac_date, vac_supplier_id, vac_quantity)
            repo.vaccines.insert(new_vac)
            repo.vaccinesCounter += 1

        for i in range(0, int(type_read_count[1])):
            data_line = config_file.readline().split(',')
            sup_id = int(data_line[0])
            sup_name = data_line[1]
            sup_log = int(data_line[2])

            # create supplier in the table
            new_sup = Supplier(sup_id, sup_name, sup_log)
            repo.suppliers.insert(new_sup)

        for i in range(0, int(type_read_count[2])):
            data_line = config_file.readline().split(',')
            clinic_id = int(data_line[0])
            clinic_name = data_line[1]
            clinic_demand = int(data_line[2])
            clinic_log = int(data_line[3])

            # create clinic in the table
            new_clinic = Clinic(clinic_id, clinic_name, clinic_demand, clinic_log)
            repo.clinics.insert(new_clinic)

        for i in range(0, int(type_read_count[3])):
            data_line = config_file.readline().split(',')
            log_id = int(data_line[0])
            log_name = data_line[1]
            log_count_sent = int(data_line[2])
            log_count_rec = int(data_line[3])

            # create logistic in the table
            new_log = Logistic(log_id, log_name, log_count_rec, log_count_sent)
            repo.logistics.insert(new_log)

def receiveShipment(supplierName, amount, date):
    # Adding the new vaccine shipment's details to the vaccines table
    supplier = repo.suppliers.find_supplier_by_name(supplierName)
    repo.vaccines.insert(Vaccine(repo.vaccinesCounter, date, supplier.id, int(amount)))
    repo.vaccinesCounter += 1
    # Increasing the amount of vaccines received through the current logistic
    logistic = repo.logistics.find_logistic_by_supplier(supplier.logistic)
    repo.logistics.update_count_received(logistic.count_received + int(amount), logistic.id)
    repo._conn.commit()


def sendShipment(location, amount):
    # Decreasing the amount of vaccines demanded by the current clinic
    clinic = repo.clinics.find_clinic_by_location(location)
    repo.clinics.update_demand(clinic.demand - int(amount), location)
    # Increase the amount of vaccines sent by the current logistic
    logistic = repo.logistics.find_logistic_by_clinic(clinic.logistic)
    repo.logistics.update_count_sent(logistic.count_sent + int(amount), logistic.id)
    # Collecting the vaccines from the vaccines table according to the instructions

    # Sorts the vaccine table in order to deal with older shipment prior to the newer
    all_vacs = repo.vaccines.find_all()
    sorted_all_vacs = sorted(all_vacs, key=lambda x: x.date)
    # date_values = list(map(lambda x: x.date, sorted_all_vacs))
    # repo.vaccineSort()
    # c = repo._conn.cursor()
    # # select_all executes SELECT* FROM table via the cursor c
    # repo.vaccines.select_all(c)
    # vaccine is a list representing a line in the vaccines table
    # find_next is a new method in DAO whichs returns the next line in the table
    count_amount = int(amount)
    count_loop = 0
    while count_loop < len(sorted_all_vacs) and count_amount != 0:
        # Vaccine[3] is the quantity of the current vaccine shipment we are dealing with
        if count_amount >= sorted_all_vacs[count_loop].quantity:
            count_amount = count_amount - sorted_all_vacs[count_loop].quantity
            repo.vaccines.delete_vaccine(sorted_all_vacs[count_loop].id)
            count_loop += 1
            repo._conn.commit()
        # If there are more vaccines in the current shipment than the required amount we are done collecting them
        # current vaccine shipments quantity - amount is the number of remaining vaccines after the collecting
        else:
            repo.vaccines.update_quantity(sorted_all_vacs[count_loop].quantity - int(count_amount), sorted_all_vacs[count_loop].id)
            count_amount = 0
            repo._conn.commit()



def output(output_file, order_file):
    outputFile = open(output_file, "w")
    with open(order_file) as orderfile:
       list = orderfile.readlines()
       for i in range(0, len(list)):
           order = list[i].split(",")
           if len(order) == 2:
                    # Send shipment order <location>,<amount>
              sendShipment(order[0], order[1])
           else:
                    # Receive shipment order <name>,<amount>,<date>
              dates = order[2].split("-")
              receiveShipment(order[0], order[1], datetime(int(dates[0]), int(dates[1]), int(dates[2])))
           outputFile.write(
               str(repo.getInventory()) + "," + str(repo.getTotalDemand()) + ","
               + str(repo.getTotalReceived()) + "," + str(repo.getTotalSent()) + '\n')

if __name__ == '__main__':
    main(sys.argv)
