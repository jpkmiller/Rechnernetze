from threading import Thread

from Praxis.Aufgabe1_RealTime.src import GLOBAL_VALUES
from Praxis.Aufgabe1_RealTime.src.Logger import Logger as L
from Praxis.Aufgabe1_RealTime.src.KundIn import KundIn
from Praxis.Aufgabe1_RealTime.src.Station import Station
import time

bakery = Station('Bäcker', 10 * GLOBAL_VALUES.FACTOR)
butcher = Station('Metzger', 30 * GLOBAL_VALUES.FACTOR)
cheese = Station('Käse', 60 * GLOBAL_VALUES.FACTOR)
checkout = Station('Kasse', 5 * GLOBAL_VALUES.FACTOR)
L.add_station_list([bakery, butcher, cheese, checkout])

typ_a_customers = []
typ_b_customers = []


def type_a_generator():
    count = 0
    print("a started")
    while True:
        count += 1
        T1 = KundIn([
            # (Zeit von A nach B, max. Schlange, Anz. Einkäufe)
            (10 * GLOBAL_VALUES.FACTOR, 10, 10, bakery),
            (30 * GLOBAL_VALUES.FACTOR, 10, 5, butcher),
            (45 * GLOBAL_VALUES.FACTOR, 5, 3, cheese),
            (60 * GLOBAL_VALUES.FACTOR, 20, 30, checkout),
        ], 200 * GLOBAL_VALUES.FACTOR, 'A', count)
        typ_a_customers.append(T1)
        L.add_customer(T1)
        T1.start()
        if time.time() + 200 * GLOBAL_VALUES.FACTOR - GLOBAL_VALUES.start_time > 30 * 60 * GLOBAL_VALUES.FACTOR:
            return
        time.sleep(200 * GLOBAL_VALUES.FACTOR)


def type_b_generator():
    count = 0
    print("b started")
    while True:
        count += 1
        T2 = KundIn([
            (30 * GLOBAL_VALUES.FACTOR, 5, 2, butcher),
            (30 * GLOBAL_VALUES.FACTOR, 20, 3, checkout),
            (20 * GLOBAL_VALUES.FACTOR, 20, 3, bakery),
        ], 60 * GLOBAL_VALUES.FACTOR, 'B', count)
        typ_b_customers.append(T2)
        L.add_customer(T2)
        T2.start()
        if time.time() + 60 * GLOBAL_VALUES.FACTOR - GLOBAL_VALUES.start_time > 30 * 60 * GLOBAL_VALUES.FACTOR:
            return
        time.sleep(60 * GLOBAL_VALUES.FACTOR)


if __name__ == "__main__":
    start_time = time.time()
    bakery.start()
    butcher.start()
    cheese.start()
    checkout.start()

    thread_a = Thread(target=type_a_generator)
    thread_b = Thread(target=type_b_generator)

    GLOBAL_VALUES.start_time = time.time()
    L.set_start_time(GLOBAL_VALUES.start_time)

    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()
    for customer in typ_b_customers:
        customer.join()
        print(customer)
    for customer in typ_a_customers:
        customer.join()

    bakery.keep_running = False
    bakery.start_serve_event.set()
    butcher.keep_running = False
    butcher.start_serve_event.set()
    cheese.keep_running = False
    cheese.start_serve_event.set()
    checkout.keep_running = False
    checkout.start_serve_event.set()

    bakery.join()
    butcher.join()
    cheese.join()
    checkout.join()

    print("simulation finished. \n took: {}".format((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR))
    L.set_end_time(time.time())
    KundIn.output_file.close()
    Station.output_file.close()

    L.add_station_list([bakery, butcher, cheese, checkout])
    L.log('supermarket.txt')
