from Praxis.Aufgabe1_RealTime.src import GLOBAL_VALUES
import threading
import time

simulationTimeL = threading.Lock()
customer_listL = threading.Lock()
station_listL = threading.Lock()


class Logger:
    # current time of simulation
    simulation_time = 0
    start_time = 0
    end_time = 0
    customer_list = []
    shopping_time = 0
    full_purchase_customers = 0
    full_purchase_shopping_time = 0
    station_list = []

    @staticmethod
    def log(filepath):

        for customer in Logger.customer_list:
            time_shopping = customer.time_end - customer.time_begin
            Logger.add_shopping_time(time_shopping)
            if customer.full_purchase:
                Logger.add_full_purchase_customer()
                Logger.add_full_purchase_shopping_time(time_shopping)

        file = open(file=filepath, mode="w", encoding='UTF-8')
        file.write("Simulationsdauer: {}\n".format(str((Logger.end_time - Logger.start_time) / GLOBAL_VALUES.FACTOR)))
        file.write("Anzahl Kunden: {}\n".format(str(len(Logger.customer_list))))
        file.write("Anzahl vollständige Einkäufe: {}\n".format(str(Logger.full_purchase_customers)))
        file.write("Mittlere Einkaufsdauer: {}\n".format(str(Logger.get_avg_shopping_time())))
        file.write("Mittlere Einkaufsdauer (vollständig): {}\n".format(Logger.get_avg_full_purchase_shopping_time()))

        # logging stations
        for station in Logger.station_list:
            file.write(station.name + " ausgelassen: " + str(Logger.get_drop_percentage(station)) + "%\n")

    @staticmethod
    def set_start_time(t=time.time()):
        Logger.start_time = t

    @staticmethod
    def set_end_time(t=time.time()):
        Logger.end_time = t

    @staticmethod
    def add_customer(customer):
        # thread safe
        with customer_listL:
            Logger.customer_list.append(customer)

    @staticmethod
    def add_station_list(station_list):
        # thread safe
        with station_listL:
            Logger.station_list = station_list

    # ========================= PRIVATE METHODS =========================

    @staticmethod
    def add_full_purchase_customer():
        Logger.full_purchase_customers += 1

    @staticmethod
    def add_full_purchase_shopping_time(amount):
        Logger.full_purchase_shopping_time += amount

    @staticmethod
    def add_shopping_time(amount):
        Logger.shopping_time += amount

    @staticmethod
    def get_avg_full_purchase_shopping_time():
        return (Logger.full_purchase_shopping_time / Logger.full_purchase_customers) / GLOBAL_VALUES.FACTOR

    @staticmethod
    def get_avg_shopping_time():
        return (Logger.shopping_time / len(Logger.customer_list)) / GLOBAL_VALUES.FACTOR

    @staticmethod
    def get_drop_percentage(station):
        return (station.get_amount_skipped_customers() /
                (station.get_amount_customers() + station.get_amount_skipped_customers())) * 100
