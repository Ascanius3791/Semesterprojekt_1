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
        self.type_of_train = "ICE" if "ICE " in self.name else "RE" if "RE " in self.name else "RB" if "RB " in self.name else "IC" if "IC " in self.name else "S" if "S " in self.name else "STR" if "STR " in self.name else  "U" if "U " in self.name else "Bus" if "Bus " in self.name else "unknown"

    def convert_delay_to_minutes(self,delay):
        if(delay == None):
            return 0
        minutes = 0
        letters = list(str(delay))
        minutes = 60*int(letters[0]) + 10*int(letters[2]) + int(letters[2])
        return minutes 
    def print(self):
        print("Train_ID: ",self.Train_ID)
        print("departure: ",self.departure)
        print("delay: ",self.delay)
        print("cancelled: ",self.cancelled)
        print("destination: ",self.destination)
        print("type_of_train: ",self.type_of_train)
        print("name: ",self.name)
        print("\n")
    
    
class analysis:
    trains = []
    allowed_types = ["ICE","RE","S","U","STR","Bus","IC","RB","unknown"]
    
    def train_count(self):
        print("Number of trains: ",len(self.trains))
        return len(self.trains)
    
    def cancellations_by_type(self):
        cancelled_ICE=0
        cancelled_RE=0
        cancelled_S=0
        cancelled_U=0
        cancelled_STR=0
        cancelled_Bus=0
        

        total_ICE=0
        total_RE=0
        total_S=0
        total_U=0
        total_STR=0
        total_Bus=0
        
        for i in self.trains:
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
            if "U " in i.name:
                total_U +=1
                if(i.cancelled):
                    cancelled_U+=1
            if "STR " in i.name:
                total_STR +=1
                if(i.cancelled):
                    cancelled_STR+=1
            if "Bus " in i.name:
                total_Bus +=1
                if(i.cancelled):
                    cancelled_Bus+=1
         
        if(total_ICE != 0):        
            print("total_ICE: ",total_ICE , "cancelled: " ,cancelled_ICE , "that is ",100.0*cancelled_ICE/total_ICE, "%","\n")
        else:
            print("No ICE found")
        if(total_RE != 0):
            print("total_RE: ",total_RE , "cancelled: " ,cancelled_RE , "that is ",100.0*cancelled_RE/total_RE, "%","\n")
        else:
            print("No RE found")
        if(total_S != 0):
            print("total_S: ",total_S , "cancelled: " ,cancelled_S , "that is ",100.0*cancelled_S/total_S, "%","\n")
        else:
            print("No S found")
        if(total_U != 0):
            print("total_U: ",total_U , "cancelled: " ,cancelled_U , "that is ",100.0*cancelled_U/total_U, "%","\n")
        else:
            print("No U found")
        if(total_STR != 0):
            print("total_STR: ",total_STR , "cancelled: " ,cancelled_STR , "that is ",100.0*cancelled_STR/total_STR, "%","\n")
        else:
            print("No STR found")
        if(total_Bus != 0):
            print("total_Bus: ",total_Bus , "cancelled: " ,cancelled_Bus , "that is ",100.0*cancelled_Bus/total_Bus, "%","\n")
        else:
            print("No Bus found")
            
    def average_delay_by_type(self,type_of_train):
        if(type_of_train not in self.allowed_types):
            print("Invalid type of train")
            return
        total_delay = 0
        total_trains = 0
        for i in self.trains:
            if i.type_of_train == type_of_train:
                total_delay += i.delay
                total_trains += 1
        if(total_trains != 0):
            print("average delay of ",type_of_train,": ",total_delay/total_trains)
        else:
            print("No ",type_of_train," found")
        return total_delay/total_trains
        
            
    
#print(client.locations("Frankfurt(Main)Hbf")[0].id) #example of how to access the info about the self.tation
#input("Press Enter to continue...\n\n")


train_info = client.departures(
    station=station_ID,
    date=datetime.datetime.now(),
    max_trips=1000 #about 4500 trains are the maximum available (testet at 00:00)
)


print(train_info[0])            #the [0] gets the info about the 0-th train
Trains = [Train(client_departures) for client_departures in train_info]


print("There are" ,len(Trains), "Trains to be found here.")
input("Press Enter")

Trains[0].print()
Trains[1].print()

analysis = analysis()
analysis.trains = Trains
analysis.cancellations_by_type()
analysis.average_delay_by_type("ICE")
analysis.average_delay_by_type("RE")
analysis.average_delay_by_type("S")
analysis.average_delay_by_type("U")
analysis.average_delay_by_type("STR")
analysis.average_delay_by_type("Bus")
analysis.average_delay_by_type("unknown")

