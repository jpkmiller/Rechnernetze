import heapq
from collections import namedtuple
from Aufgabe1.src.Logger import Logger as L


class EventList:
    event_queue = []
    event_number = 0
    heapq.heapify(event_queue)
    Event = namedtuple(typename='event', field_names=['eTime', 'ePrio', 'eNum', 'eFun', 'eArgs'], rename=False)

    @staticmethod
    def next():
        EventList.event_number += 1
        return EventList.event_number

    @staticmethod
    def pop():
        if len(EventList.event_queue) > 0:
            return heapq.heappop(EventList.event_queue)
        return ()

    @staticmethod
    def push(event):
        heapq.heappush(EventList.event_queue, event)

    @staticmethod
    def start():
        while len(EventList.event_queue) > 0 and EventList.event_number < 1000:
            e = EventList.pop()
            L.simulation_time = e.eTime
            e.eFun(e.eArgs)
