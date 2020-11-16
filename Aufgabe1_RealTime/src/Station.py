from threading import Thread, Event
import time


class Station(Thread):
    start_serve_event = Event()

    def __init__(self, name, __time__=30):
        Thread.__init__(self)
        self.name = name
        self.time = __time__
        self.customer_queue = []

    def run(self):
        # TODO: when to terminate?
        while True:
            # first wait for the first customer
            self.wait_for_customer()
            # then serve while queue is empty
            # remember: serve is a recursive function!
            self.serve([])

    # just wait for somebody queues in
    def wait_for_customer(self):
        self.start_serve_event.wait()
        self.start_serve_event.clear()

    # this is the method a customer calls.
    def queue(self, customer):
        # enqueue customer
        self.customer_queue.append(customer)
        # if queue is empty, customer will get served right away.
        if len(self.customer_queue) <= 1:
            if not self.start_serve_event.is_set():
                # just wake the station and it will start serving
                self.start_serve_event.set()
        return

    # recursively serve all customer queued. Returns if queue is empty
    def serve(self, args):
        # just a safety check.
        if len(self.customer_queue) <= 0:
            return

        # sleep represents the serving
        time.sleep(self.time)
        # after serving wake the customer
        customer = self.customer_queue.pop(0)
        # to be implemented:
        # customer.finished_serve_event.set()

        # if there still are customer queued, serve the next one
        if len(self.customer_queue) > 0:
            self.serve([])

    def __repr__(self):
        return self.name
