import time
from Praxis.PeerToPeerChat.Client import Client

walter = Client('Bonito')
josef = Client('Bomser')
alex = Client('UNKNOWN')
time.sleep(1)

josef.send_message('Moin du Eumel', 'Bonito')
time.sleep(10)
walter.broadcast("lass mi in ruh!")
