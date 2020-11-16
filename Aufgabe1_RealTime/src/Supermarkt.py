from threading import Thread

from Aufgabe1_RealTime.src.KundIn import KundIn
from Aufgabe1_RealTime.src.Station import Station
import time

FACTOR = 0.1
bakery = Station('Bäcker', 10 * FACTOR)
butcher = Station('Wursttheke', 30 * FACTOR)
cheese = Station('Cheese', 60 * FACTOR)
checkout = Station('Kasse', 5 * FACTOR)

start_time = 0


def type_a_generator():
    print("a started")
    while True:
        T1 = KundIn([
            # (Zeit von A nach B, max. Schlange, Anz. Einkäufe)
            (10 * FACTOR, 10, 10, bakery),
            (30 * FACTOR, 10, 5, butcher),
            (45 * FACTOR, 5, 3, cheese),
            (60 * FACTOR, 20, 30, checkout),
        ], 200 * FACTOR, 'A')
        T1.start()
        if time.time() + 200 * FACTOR - start_time > 30 * 60 * FACTOR:
            return
        time.sleep(200 * FACTOR)


def type_b_generator():
    print("b started")
    while True:
        T2 = KundIn([
            (30 * FACTOR, 5, 2, butcher),
            (30 * FACTOR, 20, 3, checkout),
            (20 * FACTOR, 20, 3, bakery),
        ], 60 * FACTOR, 'B')
        T2.start()
        if time.time() + 60 * FACTOR - start_time > 30 * 60 * FACTOR:
            return
        time.sleep(60 * FACTOR)


if __name__ == "__main__":
    start_time = time.time()
    bakery.start()
    butcher.start()
    cheese.start()
    checkout.start()

    thread_a = Thread(target=type_a_generator)
    thread_b = Thread(target=type_b_generator)
    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()

    # EL.push(EL.Event(0, 2, EL.next(), T1.begin, []))
    # EL.push(EL.Event(1, 2, EL.next(), T2.begin, []))
    # EL.start()
