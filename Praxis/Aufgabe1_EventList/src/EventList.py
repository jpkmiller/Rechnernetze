import heapq
from collections import namedtuple
from Praxis.Aufgabe1_EventList.src.Logger import Logger as L


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
    def start(condition):
        while len(EventList.event_queue) > 0 and condition():
            e = EventList.pop()
            L.simulation_time = e.eTime
            e.eFun(e.eArgs)
