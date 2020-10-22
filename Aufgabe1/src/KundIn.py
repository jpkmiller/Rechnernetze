from Aufgabe1.src.EventList import EventList as EL
from Aufgabe1.src.Logger import Logger as L
from copy import deepcopy
from collections import namedtuple


class KundIn:

    def __init__(self, station_list, time_between_customers, typ):
        self.station_list = station_list
        self.time_between_customers = time_between_customers
        self.type = typ
        self.count = 1
        self.full_purchase = False
        self.skipped_station = False
        self.time_shopping = 0

    def add_shopping_time(self, amount):
        self.time_shopping += amount

    def begin(self, args):
        # logging
        print(str(self) + " begin at " + str(L.simulation_time))
        L.add_customer(self)

        # instantiate next Customer (copy of current customer)

        next_customer_station_list = self.station_list.copy()
        next_customer = KundIn(next_customer_station_list, self.time_between_customers, self.type)
        next_customer.count = next_customer.count + 1

        # create begin event for next customer (next customer of same type gets announced)
        begin_event = EL.Event(eTime=L.simulation_time + self.time_between_customers,
                               ePrio=2,
                               eNum=EL.next(),
                               eFun=next_customer.begin,
                               eArgs=[])

        # create event for arriving at first station of current customer
        time_to_station = self.station_list[0][0]
        arrive_event = EL.Event(eTime=L.simulation_time + time_to_station, ePrio=3,
                                eNum=EL.next(), eFun=self.arrive,
                                eArgs=[])

        self.add_shopping_time(time_to_station)

        # push created events on heap
        EL.push(begin_event)
        EL.push(arrive_event)
        return

    def arrive(self, args):

        station = self.station_list[0]
        print(str(self) + " arrive " + str(station[3]) + " at " + str(L.simulation_time))

        self.add_shopping_time(station[0])

        if len(station[3].customer_queue) < station[1]:
            station[3].queue(self)
        else:
            print(str(self) + " skipped " + str(station[3]) + " at " + str(L.simulation_time))
            self.skipped_station = True
            self.station_list.pop(0)

            arrive_event = EL.Event(eTime=L.simulation_time + station[0], ePrio=3,
                                    eNum=EL.next(), eFun=self.arrive, eArgs=[])
            EL.push(arrive_event)

    def leave(self, args):
        if len(self.station_list) <= 0:
            return
        station = self.station_list.pop(0)

        # logging
        print(str(self) + " leave " + str(station[3]) + " at " + str(L.simulation_time))

        if len(self.station_list) <= 0:
            self.full_purchase = not self.skipped_station
            return

        # create event for arriving at next station
        arrive_event = EL.Event(eTime=L.simulation_time + self.station_list[0][0], ePrio=3,
                                eNum=EL.next(), eFun=self.arrive, eArgs=[])
        EL.push(arrive_event)

    def __repr__(self):
        return self.type + "-" + str(self.count)