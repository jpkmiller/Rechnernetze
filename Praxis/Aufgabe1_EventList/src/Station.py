from Praxis.Aufgabe1_EventList.src.EventList import EventList as EL
from Praxis.Aufgabe1_EventList.src.Logger import Logger as L


class Station:
    output_file = open(file="supermarkt_station.txt", mode="w", encoding="UTF-8")
    def __init__(self, name, __time__=30):
        self.name = name
        self.time = __time__

        self.__customer_queue__ = []
        self.__amount_customer__ = 0
        self.__amount_skipped_customer__ = 0

    def add_customer(self):
        self.__amount_customer__ += 1

    def add_skipped(self):
        self.__amount_skipped_customer__ += 1

    def get_customer_queue(self):
        return self.__customer_queue__

    def get_amount_customer(self):
        return self.__amount_customer__

    def get_amount_skipped_customer(self):
        return self.__amount_skipped_customer__

    def queue(self, customer):
        print(str(L.simulation_time) + ":" + str(self) + " adding customer " + str(customer),
              file=Station.output_file)
        self.__customer_queue__.append(customer)
        self.add_customer()

        # if queue is empty, customer will get served right away.
        if len(self.__customer_queue__) <= 1:
            self.serve([])

    def serve(self, args):
        if len(self.__customer_queue__) <= 0:
            return
        customer = self.__customer_queue__[0]
        print(str(L.simulation_time) + ":" + str(self) + " serving customer " + str(customer),
              file=Station.output_file)
        leave_event = EL.Event(eTime=L.simulation_time + customer.station_list[0][2] * self.time, ePrio=1,
                               eNum=EL.next(), eFun=customer.leave, eArgs=[])
        serve_next_event = EL.Event(eTime=L.simulation_time + customer.station_list[0][2] * self.time, ePrio=1,
                                    eNum=EL.next(), eFun=self.leave, eArgs=[])
        EL.push(leave_event)
        EL.push(serve_next_event)

    def leave(self, args):
        customer = self.__customer_queue__.pop(0)
        print(str(L.simulation_time) + ":" + str(self) + " finished customer " + str(customer),
              file=Station.output_file)
        self.serve([])

    def __repr__(self):
        return self.name
