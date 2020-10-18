import heapq
from collections import namedtuple

class EventList:
    eventQueue = []
    eventNumber = 0
    simulationTime = 0
    event = namedtuple(typename='event', field_names=['eTime', 'ePrio', 'eNum', 'eFun', 'eArgs'], rename=False)
    counter = 0

    @staticmethod
    def __init__(__list__):
        EventList.eventQueue = __list__
        heapq.heapify(EventList.eventQueue)

    @staticmethod
    def next():
        EventList.counter = EventList.counter + 1
        return EventList.counter

    @staticmethod
    def pop():
        if len(EventList.eventQueue) > 0:
            return heapq.heappop(EventList.eventQueue)
        return ()

    @staticmethod
    def push(event):
        heapq.heappush(EventList.eventQueue, event)

    @staticmethod
    def start():
        while len(EventList.eventQueue) > 0:
            EventList.eventNumber += 1
            ereignis = EventList.pop()
            # ereignis 3 ist der lambda Ausdruck
            # ereignis 4 sind die lambda Argumente
            ereignis[3](ereignis[4][0], ereignis[4][1])
