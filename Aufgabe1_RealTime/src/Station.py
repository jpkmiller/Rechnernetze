from threading import Thread, Event
import time


class Station(Thread):
    def __init__(self, name, __time__=30):
        Thread.__init__(self)
        self.name = name
        self.serving_time = __time__
        self.customer_queue = []
        self.start_serve_event = Event()

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
        print(str(customer) + " waits at station " + str(self))
        # enqueue customer
        self.customer_queue.append(customer)
        # if queue is empty, customer will get served right away.
        if len(self.customer_queue) <= 1:
            # if not self.start_serve_event.is_set():
                # just wake the station and it will start serving
            self.start_serve_event.set()
        return

    # recursively serve all customer queued. Returns if queue is empty
    def serve(self, args):
        # just a safety check.
        if len(self.customer_queue) <= 0:
            return

        # get the next customer, but do not dequeue it.
        customer = self.customer_queue[0]
        print("start serving " + str(customer))
        # sleep represents the serving
        time.sleep(self.serving_time * customer.station_list[0][2])
        # dequeue customer
        self.customer_queue.pop(0)
        # after serving wake the customer
        print("finished serving " + str(customer) + " try to wake")
        customer.finished_serve_event.set()

        # if there still are customer queued, serve the next one
        if len(self.customer_queue) > 0:
            self.serve([])

    def __repr__(self):
        return self.name
