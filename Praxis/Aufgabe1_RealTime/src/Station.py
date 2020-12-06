from threading import Thread, Event, Lock
import time

from Praxis.Aufgabe1_RealTime.src import GLOBAL_VALUES


class Station(Thread):
    output_file = open("supermarket_station.txt", mode="w", encoding="UTF-8")

    def __init__(self, name, __time__=30):
        Thread.__init__(self)
        self.name = name
        self.serving_time = __time__
        self.customer_queue = []
        self.start_serve_event = Event()
        self.keep_running = True
        self.lock = Lock()

        # statistics
        self.amount_skipped = 0
        self.amount_customers = 0


    def run(self):
        while self.keep_running:
            # first wait for the first customer
            self.wait_for_customer()
            # then serve while queue is empty
            # remember: serve is a recursive function!
            self.serve([])

    def add_skipped(self):
        self.amount_skipped += 1

    def add_customer(self):
        self.amount_customers += 1

    def get_amount_customers(self):
        return self.amount_customers

    def get_amount_skipped_customers(self):
        return self.amount_skipped

    # just wait for somebody queues in
    def wait_for_customer(self):
        self.start_serve_event.wait()
        self.start_serve_event.clear()

    # this is the method a customer calls.
    def queue(self, customer):
        print(str(round((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR)) + ":" + str(
            self) + " adding customer " + str(customer), file=Station.output_file)
        # enqueue customer
        self.add_customer()
        self.lock.acquire()
        self.customer_queue.append(customer)
        # if queue is empty, customer will get served right away.
        if len(self.customer_queue) <= 1:
            # if not self.start_serve_event.is_set():
            # just wake the station and it will start serving
            self.start_serve_event.set()
        self.lock.release()
        return

    # recursively serve all customer queued. Returns if queue is empty
    def serve(self, args):
        # just a safety check.
        self.lock.acquire()
        if len(self.customer_queue) <= 0:
            return

        # get the next customer, but do not dequeue it.
        customer = self.customer_queue[0]
        self.lock.release()
        print(str(round((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR)) + ":" + str(
            self) + " serving customer " + str(customer), file=Station.output_file)
        # sleep represents the serving
        time.sleep(self.serving_time * customer.station_list[0][2])
        # dequeue customer
        print(str(round((time.time() - GLOBAL_VALUES.start_time) / GLOBAL_VALUES.FACTOR)) + ":" + str(
            self) + " finished customer " + str(customer), file=Station.output_file)
        self.lock.acquire()
        self.customer_queue.pop(0)
        # after serving wake the customer
        customer.finished_serve_event.set()

        # if there still are customer queued, serve the next one

        if len(self.customer_queue) > 0:
            self.lock.release()
            self.serve([])
        else:
            self.lock.release()

    def __repr__(self):
        return self.name
