from typing import Tuple


class Ereignis:

    def __init__(self, eventNumber, eventEntry, eventPriority, eventFunction, eventArgs=[]):
        self.event = Tuple[eventNumber, eventEntry, eventPriority, eventFunction]
        self.args = eventArgs