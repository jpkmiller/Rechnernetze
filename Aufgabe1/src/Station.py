from Aufgabe1.src.EventList import EventList as EL


class Station:

    def __init__(self, name, __time__=30):
        self.name = name
        self.time = __time__
        self.customer_queue = []

    def queue(self, customer):
        self.customer_queue.append(customer)
        # if queue is was empty, customer will get served right away.
        if len(self.customer_queue) <= 1:
            self.serve()
        return

    def serve(self):
        customer = self.customer_queue.pop(0)
        leave_event = EL.Event(eTime=EL.simulation_time + customer.station_list[0][2] * self.time, ePrio=1,
                               eNum=EL.next(), eFun=customer.leave, eArgs=[])
        EL.push(leave_event)

    def __repr__(self):
        return self.name
