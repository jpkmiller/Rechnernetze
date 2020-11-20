from Aufgabe1_RealTime.src import GLOBAL_VALUES
from Aufgabe1_RealTime.src.EventList import EventList as EL
from copy import deepcopy
from threading import Thread, Event
import time


class KundIn(Thread):
    output_file = open("supermarket_customer.txt", mode="w", encoding="UTF-8")

    def __init__(self, station_list, time_between_customers, typ, count):
        Thread.__init__(self)
        self.station_list = station_list
        self.time_between_customers = time_between_customers
        self.type = typ
        self.count = count
        self.finished_serve_event = Event()

    def run(self):
        # customer enters the system
        self.begin([])
        return

    def begin(self, args):
        print(str(self) + " begins")
        # sleep until customer arrives at first station
        time.sleep(self.station_list[0][0])
        self.arrive([])
        return

    def arrive(self, args):
        # get the next station
        station = self.station_list[0]

        # check if stations queue is too long for costumer
        if len(station[3].customer_queue) <= station[1]:
            # if not enqueue
            print(str(round((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR)) + ":" + str(
                self) + " Queueing at " + station[3].name, file=KundIn.output_file)
            station[3].queue(self)
            # wait until station has served this customer
            self.finished_serve_event.wait()
            print(str(round((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR)) + ":" + str(
                self) + " Finished at " + station[3].name, file=KundIn.output_file)
            # clear the event
            self.finished_serve_event.clear()
        else:
            print(str(round((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR)) + ":" + str(
                self) + " Dropped at " + station[3].name, file=KundIn.output_file)
        # leave current station
        self.leave([])

    def leave(self, args):
        # station is done. Remove it from station list
        station = self.station_list.pop(0)

        # station list is empty -> purchase completed
        if len(self.station_list) <= 0:
            return

        # wait until next station is reached
        time.sleep(self.station_list[0][0])
        # start purchase at next station
        self.arrive([])

    def __repr__(self):
        return self.type + str(self.count)
