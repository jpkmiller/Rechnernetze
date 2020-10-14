import heapq


class EreignisListe:
    eventQueue = []
    eventNumber = 0
    simulationTime = 0

    @staticmethod
    def __init__(__list__):
        EreignisListe.eventQueue = heapq.heapify(__list__)

    @staticmethod
    def pop():
        if len(EreignisListe.eventQueue) > 0:
            return heapq.heappop(EreignisListe.eventQueue)
        return ()

    @staticmethod
    def push(event):
        heapq.heappush(EreignisListe.eventQueue, event)

    @staticmethod
    def start():
        while len(EreignisListe.eventQueue) > 0:
            EreignisListe.eventNumber += 1
            EreignisListe