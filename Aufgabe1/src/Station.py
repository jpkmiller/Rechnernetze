from Aufgabe1.src.EventList import EventList


class Station:

    def __init__(self, name, __time__=30):
        self.name = name
        self.time = __time__
        self.customer_queue = []

    def queue(self, customer):
        self.customer_queue.append(customer)

        self.serve()

    def serve(self):
        if len(self.customer_queue) != 1:
            return
        customer = self.customer_queue[0]
        leave_event = EventList.event(eTime=EventList.simulationTime + customer.stationList[0][2] * self.time,
                                      ePrio=1, eNum=EventList.next(), eFun=customer.leave, eArgs=[])
        EventList.push(leave_event)
        return

        # amountRemainingItems = amount_items
        # while amountRemainingItems > 0:
        #     amountRemainingItems -= 1
        # time.sleep(self.time)
