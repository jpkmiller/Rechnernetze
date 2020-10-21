from Aufgabe1.src.EventList import EventList as EL
from copy import deepcopy
from threading import Thread
import time

class KundIn(Thread):

    def __init__(self, station_list, time_between_customers, type):
        Thread.__init__(self)
        self.station_list = station_list
        self.time_between_customers = time_between_customers
        self.type = type
        self.count = 1

    def begin(self, args):
        # KundIn-Threads start at the beginning of shopping
        #self.start()

        print(str(self) + " begin at " + str(EL.simulation_time))
        # instantiate next Customer (copy of current customer)
        next_customer = deepcopy(self)
        next_customer.count = next_customer.count + 1
        # create begin event for next customer (next customer of same type gets announced)
        begin_event = EL.Event(eTime=EL.simulation_time + self.time_between_customers,
                               ePrio=2,
                               eNum=EL.next(),
                               eFun=next_customer.begin,
                               eArgs=[])
        # create event for arriving at first station of current customer
        time_to_station = self.station_list[0][0]
        arrive_event = EL.Event(eTime=EL.simulation_time + time_to_station, ePrio=3,
                                eNum=EL.next(), eFun=self.arrive,
                                eArgs=[])
        # push created events on heap
        EL.push(begin_event)
        EL.push(arrive_event)
        return

    def arrive(self, args):

        station = self.station_list[0]
        print(str(self) + " arrive " + str(station[3]) + " at " + str(EL.simulation_time))

        if len(station[3].customer_queue) < station[1]:
            station[3].queue(self)
        else:
            self.station_list.pop(0)

            arrive_event = EL.Event(eTime=EL.simulation_time + station[0], ePrio=3,
                                    eNum=EL.next(), eFun=self.arrive, eArgs=[])
            EL.push(arrive_event)

    def leave(self, args):
        station = self.station_list.pop(0)
        print(str(self) + " leave " + str(station[3]) + " at " + str(EL.simulation_time))

        # shopping between stations is simulated by putting the thread to sleep.
        time.sleep(self.station_list[0][0])

        if len(self.station_list) <= 0:
            return
        # create event for arriving at next station
        arrive_event = EL.Event(eTime=EL.simulation_time + self.station_list[0][0], ePrio=3,
                                eNum=EL.next(), eFun=self.arrive, eArgs=[])
        EL.push(arrive_event)

    def __repr__(self):
        return "K" + self.type + "-" + str(self.count)
