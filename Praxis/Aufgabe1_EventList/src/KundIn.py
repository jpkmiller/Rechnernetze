from Praxis.Aufgabe1_EventList.src.EventList import EventList as EL
from Praxis.Aufgabe1_EventList.src.Logger import Logger as L


class KundIn:

    def __init__(self, station_list, time_between_customers, typ):
        self.station_list = station_list
        self.time_between_customers = time_between_customers
        self.type = typ
        self.count = 1
        self.full_purchase = False
        self.skipped_station = False

        self.time_begin = L.simulation_time
        self.time_end = L.simulation_time

    def begin(self, args):
        # add customer to Logger
        L.add_customer(self)

        # instantiate next Customer (copy of current customer)

        next_customer_station_list = self.station_list.copy()
        next_customer = KundIn(next_customer_station_list, self.time_between_customers, self.type)
        next_customer.count = self.count + 1

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

        # push created events on heap
        EL.push(begin_event)
        EL.push(arrive_event)
        return

    def arrive(self, args):
        self.time_end = L.simulation_time
        station_tuple = self.station_list[0]
        station = station_tuple[3]

        if len(station.get_customer_queue()) <= station_tuple[1]:
            print(str(L.simulation_time) + ":" + str(self) + " Queueing at " + str(station), file=open(file="supermarkt_customer.txt", mode="a", encoding="UTF-8"))
            station.queue(self)
        else:
            # logging
            print(str(L.simulation_time) + ":" + str(self) + " Dropped at " + str(station), file=open(file="supermarkt_customer.txt", mode="a", encoding="UTF-8"))

            # skipping station when number of customers in queue exceeds maximum tolerance
            self.skipped_station = True
            station.add_skipped()
            self.station_list.pop(0)

            arrive_event = EL.Event(eTime=L.simulation_time + station_tuple[0], ePrio=3,
                                    eNum=EL.next(), eFun=self.arrive, eArgs=[])
            EL.push(arrive_event)

    def leave(self, args):
        self.time_end = L.simulation_time
        if len(self.station_list) <= 0:
            return

        station_tuple = self.station_list.pop(0)
        station = station_tuple[3]

        # logging
        print(str(L.simulation_time) + ":" + str(self) + " Finished at " + str(station), file=open(file="supermarkt_customer.txt", mode="a", encoding="UTF-8"))

        if len(self.station_list) <= 0:
            self.full_purchase = not self.skipped_station
            return

        # create event for arriving at next station
        arrive_event = EL.Event(eTime=L.simulation_time + self.station_list[0][0], ePrio=3,
                                eNum=EL.next(), eFun=self.arrive, eArgs=[])
        EL.push(arrive_event)

    def __repr__(self):
        return self.type + str(self.count)
