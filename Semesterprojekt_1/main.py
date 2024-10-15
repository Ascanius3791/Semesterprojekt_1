#!/usr/bin/env python3

import datetime
from pyhafas import HafasClient
from pyhafas.profile import DBProfile

client = HafasClient(DBProfile())
station_ID = client.locations("Frankfurt(Main)Hbf")[0].id

class Train:
    Train_ID = ""
    departure = ""
    delay = 0
    cancelled = False
    destination = ""
    type_of_train = ""

print(client.locations("Frankfurt(Main)Hbf")[0].id)
input("Press Enter to continue...\n\n")
stuff = client.departures(
    station=station_ID,
    date=datetime.datetime.now(),
    max_trips=10
)
print(stuff[0])
Trains = []
for i in stuff:
    train = Train()
    train.Train_ID = i.name
    train.delay = i.delay
    train.cancelled = i.cancelled
    train.departure = i.dateTime
    
    
    Trains.append(train)
for i in Trains:
    print(i.Train_ID)
    print(i.delay)
    print(i.cancelled)
    print(i.departure)
    print("\n")

