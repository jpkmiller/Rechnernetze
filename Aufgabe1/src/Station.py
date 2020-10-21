from Aufgabe1.src.EventList import EventList as EL
from threading import Thread, Lock

lock = Lock()


class Station(Thread):

    def __init__(self, name, __time__=30):
        Thread.__init__(self)
        self.name = name
        self.time = __time__
        self.customer_queue = []

    def run(self):
        # TODO: implement run method
        return

    def queue(self, customer):
        self.customer_queue.append(customer)
        # if queue is empty, customer will get served right away.
        if len(self.customer_queue) <= 1:
            self.serve([])
        return

    def serve(self, args):
        # FIXME: the time it takes to service a customer is simulated by the station thread going to sleep for the
        #  duration of the service. time.sleep(self.time)
        # time.sleep(self.time)

        if len(self.customer_queue) <= 0:
            return
        customer = self.customer_queue.pop(0)
        leave_event = EL.Event(eTime=EL.simulation_time + customer.station_list[0][2] * self.time, ePrio=1,
                               eNum=EL.next(), eFun=customer.leave, eArgs=[])
        serve_next_event = EL.Event(eTime=EL.simulation_time + customer.station_list[0][2] * self.time, ePrio=1,
                                    eNum=EL.next(), eFun=self.serve, eArgs=[])
        EL.push(leave_event)
        EL.push(serve_next_event)

    def __repr__(self):
        return self.name
