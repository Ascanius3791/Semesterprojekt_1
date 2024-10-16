#!/usr/bin/env python3

import string
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
    name = ""
    
    
    def __init__(self,client_departures): 
        self.Train_ID = client_departures.id
        self.delay = self.convert_delay_to_minutes(client_departures.delay)
        self.cancelled = client_departures.cancelled
        self.departure = client_departures.dateTime
        self.destination = client_departures.direction
        self.name = client_departures.name
        self.type_of_train = "ICE" if "ICE " in self.name else "RE" if "RE " in self.name else "S" if "S " in self.name else "STR" if "STR " in self.name else  "U" if "U " in self.name else "Bus" if "Bus " in self.name else "unknown"

    def convert_delay_to_minutes(self,delay):
        if(delay == None):
            return 0
        minutes = 0
        letters = list(str(delay))
        minutes = 60*int(letters[0]) + 10*int(letters[2]) + int(letters[2])
        return minutes 
    
#print(client.locations("Frankfurt(Main)Hbf")[0].id) #example of how to access the info about the trainstation
#input("Press Enter to continue...\n\n")
train_info = client.departures(
    station=station_ID,
    date=datetime.datetime.now(),
    max_trips=10 #about 4500 trains are the maximum available (testet at 00:00)
)


print(train_info[0])            #the [0] gets the info about the 0-th train
Trains = [Train(client_departures) for client_departures in train_info]


print("There are" ,len(Trains), "Trains to be found here.")
input("Press Enter")

for i in Trains:
    print(i.name)
    print(i.type_of_train)
    print(i.delay)
    print(i.cancelled)
    print(i.departure)
    print("\n")

cancelled_ICE=0
cancelled_RE=0
cancelled_S=0

total_ICE=0
total_RE=0
total_S=0
for i in Trains:
    if "ICE " in i.name:
        total_ICE +=1
        if(i.cancelled):
            cancelled_ICE+=1
    if "RE " in i.name:
        total_RE +=1
        if(i.cancelled):
            cancelled_RE+=1
    if "S " in i.name:
        total_S +=1
        if(i.cancelled):
            cancelled_S+=1
print("total_ICE: ",total_ICE , "cancelled: " ,cancelled_ICE , "that is ",100.0*cancelled_ICE/total_ICE, "%","\n")
print("total_RE: ",total_RE , "cancelled: " ,cancelled_RE , "that is ",100.0*cancelled_RE/total_RE, "%","\n")
print("total_S: ",total_S , "cancelled: " ,cancelled_S , "that is ",100.0*cancelled_S/total_S, "%","\n")
    


