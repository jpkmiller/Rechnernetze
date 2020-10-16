import time


class Station:

    def __init__(self, name, __time__=30):
        self.name = name
        self.time = time
        self.customer_queue = []

    def queue(self, kundin):
        if self.customer_queue.length > 0:
            self.customer_queue.append(kundin)
        else:
            self.serve(kundin)

    def serve(self, amountItems):
        amountRemainingItems = amountItems
        while amountRemainingItems > 0:
            amountRemainingItems -= 1
            time.sleep(self.time)
