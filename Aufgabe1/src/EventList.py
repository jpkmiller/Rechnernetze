import heapq
from collections import namedtuple


class EventList:
    event_queue = []
    eventNumber = 0
    simulationTime = 0
    event = namedtuple('e', 'eTime, ePrio, eNum, eFun, eArgs')
    counter = 0

    @staticmethod
    def __init__(__list__):
        EventList.event_queue = __list__
        heapq.heapify(EventList.event_queue)

    @staticmethod
    def next():
        EventList.counter = EventList.counter + 1
        return EventList.counter

    @staticmethod
    def pop():
        if len(EventList.event_queue) > 0:
            return heapq.heappop(EventList.event_queue)
        return

    @staticmethod
    def push(event: event):
        EventList.counter += 1
        if EventList.simulationTime > 1000:
            return
        heapq.heappush(EventList.event_queue, event)

    @staticmethod
    def start():
        EventList.index = 0
        while len(EventList.event_queue) > 0:
            l = EventList.event_queue
            e = EventList.pop()
            EventList.simulationTime = e.eTime
            print(e)
            e.eFun(e.eArgs)

            # EreignisListe.eventNumber += 1
            # ereignis = EreignisListe.pop()
            # ereignis 3 ist der lambda Ausdruck
            # ereignis 4 sind die lambda Argumente
            # ereignis[3](ereignis[4][1], ereignis[4][0])
