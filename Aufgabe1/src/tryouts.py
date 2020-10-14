# %% Testcell
from collections import namedtuple

from Aufgabe1.src.EreignisListe import EreignisListe

eventList = EreignisListe([])
event = namedtuple('e', 'eTime, ePrio, eNum, eFun, eArgs')


def test(x):
    print(x)
    eventList.push(event=event(10, 0, 0, lambda: print(0), 0))


a = event(0, 0, 0, test, 0)
b = event(1, 0, 1, test, 0)

eventList = EreignisListe([a, b])
eventList.start()
