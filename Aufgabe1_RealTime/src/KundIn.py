from Aufgabe1_RealTime.src.EventList import EventList as EL
from copy import deepcopy
from threading import Thread, Event
import time


class KundIn(Thread):
    def __init__(self, station_list, time_between_customers, typ):
        Thread.__init__(self)
        self.station_list = station_list
        self.time_between_customers = time_between_customers
        self.type = typ
        self.count = 1
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
        print(str(self) + " arrive " + str(station[3]) + " at " + str(EL.simulation_time))

        # check if stations queue is too long for costumer
        if len(station[3].customer_queue) < station[1]:
            # if not enqueue
            station[3].queue(self)
            # wait until station has served this customer
            self.finished_serve_event.wait()
            # clear the event
            self.finished_serve_event.clear()
        # leave current station
        self.leave([])

    def leave(self, args):
        # station is done. Remove it from station list
        station = self.station_list.pop(0)
        print(str(self) + " leave " + str(station[3]) + " at " + str(EL.simulation_time))

        # station list is empty -> purchase completed
        if len(self.station_list) <= 0:
            return

        # wait until next station is reached
        time.sleep(self.station_list[0][0])
        # start purchase at next station
        self.arrive([])

    def __repr__(self):
        return "K" + self.type + "-" + str(self.count)
