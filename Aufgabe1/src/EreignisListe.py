import heapq


class EreignisListe:
    eventQueue = []
    eventNumber = 0
    simulationTime = 0

    @staticmethod
    def __init__(__list__):
        EreignisListe.eventQueue = __list__
        heapq.heapify(EreignisListe.eventQueue)

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
            ereignis = EreignisListe.pop()
            # ereignis 3 ist der lambda Ausdruck
            # ereignis 4 sind die lambda Argumente
            ereignis[3](ereignis[4][0], ereignis[4][1])
