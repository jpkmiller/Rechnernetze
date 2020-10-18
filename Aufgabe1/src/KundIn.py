import Aufgabe1.src.EventList as EL


class KundIn:

    def __init__(self, station_list, time_between_customers):
        self.station_list = station_list
        self.time_between_customers = time_between_customers

    def begin(self, station):
        # instantiate next Customer (copy of current customer)
        next_customer = KundIn(self.stationList, self.time_between_customers)
        # create begin event for next customer (next customer of same type gets announced)
        begin_event = EL.event(eTime=EL.simulationTime + self.time_between_customers,
                               ePrio=2,
                               eNum=EL.next(),
                               eFun=next_customer.begin,
                               eArgs=[])
        # create event for arriving at first station of current customer
        time_to_station = self.stationList[0][0]
        arrive_event = EL.event(eTime=EL.simulationTime + time_to_station, ePrio=3,
                                eNum=EL.next(), eFun=self.arrive,
                                eArgs=[])
        # push created events on heap
        EL.push(begin_event)
        EL.push(arrive_event)
        return

    def arrive(self):
        station = self.station_list[0]

        if len(station[3].customer_queue) < station[1]:
            station[3].queue(self)
        else:
            self.station_list.pop()

            arrive_event = EL.event(eTime=EL.simulationTime + station[0], ePrio=3,
                                    eNum=EL.next(), eFun=self.arrive, eArgs=[])
            EL.push(arrive_event)

    def leave(self):
        self.station_list.pop()

        arrive_event = EL.event(eTime=EL.simulationTime + self.station_list[0][0], ePrio=3,
                                eNum=EL.next(), eFun=self.arrive, eArgs=[])
        EL.push(arrive_event)
