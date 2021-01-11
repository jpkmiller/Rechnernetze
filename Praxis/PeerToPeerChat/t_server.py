import time
from Praxis.PeerToPeerChat.Client import Client

alex = Client('alex', SERVER_IP='141.37.200.32')
walter = Client('walter', SERVER_IP='141.37.200.32')
time.sleep(1)

walter.send_message('Moin du Eumel', 'alex')
time.sleep(10)
alex.broadcast("lass mi in ruh!")
