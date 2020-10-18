from Aufgabe1.src.EventList import EventList as EL
import time


class Station:

    def __init__(self, name, __time__=30):
        self.name = name
        self.time = time
        self.customer_queue = []

    def queue(self, kundin):
        # add customer to queue
        self.queue.append(kundin)
        if len(self.customer_queue) == 0:
            self.serve()
        return

    def serve(self):
        # customer has to be removed from serve_queue
        customer = self.customer_queue.pop()
        leave_event = EL.event(eTime=EL.simulationTime + customer.stationList[0][2] * self.time, ePrio=1, eNum=EL.next(), eFun=customer.leave, eArgs=[])
        EL.push(leave_event)
