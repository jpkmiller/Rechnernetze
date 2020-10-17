from Aufgabe1.src.EventList import EventList


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
        # check if queue is empty
        # todo: rethinking needed. Probably a busy flag would be a better approach
        if len(self.customer_queue) <= 0:
            return
        # get the customer
        customer = self.customer_queue[0]
        # create event when the customer has to leave the station aka when he got served
        leave_event = EventList.event(eTime=EventList.simulationTime + customer.stationList[0][2] * self.time,
                                      ePrio=1, eNum=EventList.next(), eFun=customer.leave, eArgs=[])
        # push event on heap
        EventList.push(leave_event)
        # reminder: customer has not finished with this station!
        # He has to stay inside the queue until the leave_event gets processed
        return

        # amountRemainingItems = amount_items
        # while amountRemainingItems > 0:
        #     amountRemainingItems -= 1
        # time.sleep(self.time)
