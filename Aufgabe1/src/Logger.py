class Logger:
    simulation_time = 0
    simulation_finished = 0
    simulation_amount_customer = 0
    simulation_amount_shopping_complete = 0
    simulation_time_shopping = 0
    simulation_time_shopping_complete = 0

    @staticmethod
    def log(filepath):
        file = open(filepath, "w")
        file.write("Simulationsende: " + str(Logger.simulation_time) + "\n")
        file.write("Anzahl Kunden: " + str(Logger.simulation_amount_customer) + "\n")
        file.write("Anzahl vollständige Einkäufe: " + str(Logger.simulation_amount_shopping_complete) + "\n")
        file.write("Mittlere Einkaufsdauer: " + str(Logger.simulation_time_shopping) + "\n")
        file.write("Mittlere Einkaufsdauer (vollständig): " + str(Logger.simulation_time_shopping_complete) + "\n")

    @staticmethod
    def add_customer():
        Logger.simulation_amount_customer += 1

    @staticmethod
    def add_amount_shopping():
        Logger.simulation_amount_shopping_complete += 1
