import Aufgabe1.src.EreignisListe as event

class KundIn:

  def __init__(self, stationList):
    self.stationList = stationList

  def begin(self, station):


  def arrive(self):
    return 0

  def leave(self):
    return 0

# •	Beginn des Einkaufs
# o	Ereignis Ankunft an der ersten Station erzeugen
# o	nächstes Ereignis Beginn des Einkaufs für den gleichen KundInnen-Typ erzeugen
# •	Ankunft an einer Station
# o	anhand der Warteschlangenlänge überprüfen, ob an der Station eingekauft wird
# o	wenn eingekauft wird, entweder Einreihen in die Warteschlange (Systemzustand ändern) oder im Falle einer direkten Bedienung das Ereignis Verlassen der Station erzeugen
# o	wenn nicht eingekauft wird, direkt das Ereignis Ankunft an der nächsten Station erzeugen
# •	Verlassen einer Station
# o	Ereignis Ankunft an der nächsten Station erzeugen
# o	wenn sich weitere KundInnnen in der Warteschlange befinden, erste KundIn aus der Warteschlange nehmen und Ereignis Verlassen der Station für die nächste KundIn erzeugen
