class Logger:
    # current time of simulation
    simulation_time = 0
    customers = 0
    customer_list = []
    shopping_time = 0
    full_purchase_customers = 0
    full_purchase_shopping_time = 0
    station_list = []

    @staticmethod
    def log(filepath):

        for customer in Logger.customer_list:
            Logger.customers += 1
            time_shopping = customer.time_end - customer.time_begin
            Logger.add_shopping_time(time_shopping)
            if customer.full_purchase:
                Logger.add_full_purchase_customer()
                Logger.add_full_purchase_shopping_time(time_shopping)

        file = open(file=filepath, mode="w", encoding='UTF-8')
        file.write("Simulationsdauer: " + str(Logger.simulation_time) + "\n")
        file.write("Anzahl Kunden: " + str(Logger.customers) + "\n")
        file.write("Anzahl vollständige Einkäufe: " + str(Logger.full_purchase_customers) + "\n")
        file.write("Mittlere Einkaufsdauer: " + str(Logger.get_shopping_time()) + "\n")
        file.write("Mittlere Einkaufsdauer (vollständig): " + str(Logger.get_full_purchase_shopping_time()) + "\n")

        # logging stations
        for station in Logger.station_list:
            file.write(station.name + " ausgelassen: " + str(Logger.get_drop_percentage(station)) + "%\n")

    @staticmethod
    def add_station_list(station_list):
        Logger.station_list = station_list

    @staticmethod
    def add_customer(customer):
        Logger.customer_list.append(customer)

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
    def get_full_purchase_shopping_time():
        return Logger.full_purchase_shopping_time / Logger.full_purchase_customers

    @staticmethod
    def get_shopping_time():
        return Logger.shopping_time / Logger.customers

    @staticmethod
    def get_drop_percentage(station):
        return (station.get_amount_skipped_customer() / (station.get_amount_customer() + station.get_amount_skipped_customer())) * 100
