# %% Testcell
from collections import namedtuple

from Praxis.Aufgabe1_EventList.src.EventList import EventList
from Praxis.Aufgabe1_EventList.src.KundIn import KundIn

eventList = EventList([])
event = namedtuple('e', 'eTime, ePrio, eNum, eFun, eArgs')
counter = 0


def begin(args: list):
    customer: KundIn = args[0]
    time: int = args[1]
    next_customer = KundIn(customer.stationList, customer.timeBetweenCustomers)
    begin_event = event(eTime=time + customer.timeBetweenCustomers, ePrio=2, eNum=++counter, eFun=begin,
                        eArgs=[next_customer])
    station = customer.stationList[customer.station_index]
    arrive_event = event(eTime=time + station[0], ePrio=3, eNum=++counter, eFun=arrive, eArgs=[])
    eventList.push(begin_event)
    eventList.push(arrive_event)
    return


def arrive():
    return


def test(x: list):
    print(x[0])
    eventList.push(event(1, 2, 2, lambda c: print("event c"), []))
    return


a = event(0, 2, 0, test, ["event a"])
b = event(1, 2, 1, lambda x: print("event b"), [])

eventList = EventList([b, a])
eventList.start()
