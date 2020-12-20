import time
from Praxis.PeerToPeerChat.Client import Client

walter = Client('Bonito')
josef = Client('Bomser')
time.sleep(1)

josef.sendMessage('Moin du Eumel', 'Bonito')
