#!/usr/bin/env python3

from operator import attrgetter
import string
import datetime
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
import time
from zoneinfo import ZoneInfo

client = HafasClient(DBProfile())
station_ID = client.locations("Frankfurt(Main)Hbf")[0].id
name_of_file = "train_info.txt"
file = open(name_of_file,"a")

class Train:
    Train_ID = "None"
    departure = "None"
    delay = 0
    cancelled = False
    destination = "None"
    type_of_train = "None"
    name = "None"
    platform = "None"
    
    
    def __init__(self,client_departures=None):
        if(client_departures is None):
            return
        self.Train_ID = client_departures.id
        self.delay = int(client_departures.delay.seconds)/60.0 if client_departures.delay is not None else 0
        self.cancelled = client_departures.cancelled
        self.departure = client_departures.dateTime
        self.destination = client_departures.direction
        self.name = client_departures.name
        self.type_of_train = "ICE" if "ICE " in self.name else "RE" if "RE " in self.name else "RB" if "RB " in self.name else "IC" if "IC " in self.name else "S" if "S " in self.name else "STR" if "STR " in self.name else  "U" if "U " in self.name else "Bus" if "Bus " in self.name else "unknown"
        self.platform = str(client_departures.platform)
    
    def print(self):
        print("Train_ID: ",self.Train_ID)
        print("departure: ",self.departure)
        print("delay: ",self.delay)
        print("cancelled: ",self.cancelled)
        print("destination: ",self.destination)
        print("type_of_train: ",self.type_of_train)
        print("name: ",self.name)
        print("platform: ",self.platform)
        print("\n")
    
    def print_to_file(self,file_name):
        file = open(file_name,"a")
        #remove the " " from the ID this is needed to make it consistent, else there are "random" amounts of " " in the ID, same goes for the destination
        self.Train_ID = self.Train_ID.replace(" ","")
        file.write(str(self.Train_ID) + " ")
        file.write(str(self.departure) + " ")
        file.write(str(self.delay) + " ")
        file.write(str(self.cancelled) + " ")
        self.destination = self.destination.replace(" ","")
        file.write(str(self.destination) + " ")
        file.write(str(self.type_of_train) + " ")
        self.name = self.name.replace(" ","")
        file.write(str(self.name) + " ")
        self.platform = self.platform.replace(" ","")
        file.write(str(self.platform) + " ")
        file.write("\n")
        
        file.close()
        
    
    def get_train_info_from_file(self,file_name,line):
        file = open(file_name,"r")
        
        for i in range(line):
            file.readline()
        info = file.readline()
        
        if(info == ""):
            file.close()
            return None
        info = info.split(" ")
        self.Train_ID = info[0]
        self.departure = info[1]+" "+info[2]
        self.delay = float(info[3])
        self.cancelled = True if info[4] == "True" else False
        self.destination = info[5]
        self.type_of_train = info[6]
        self.name = info[7]
        self.platform = info[8]
        file.close()   
        
        return True
        
class filemanagement:
    trains = []

    def __init__(self,max_numb_of_trains):
        train_info = client.departures(
        station=station_ID,
        duration=120,
        date=datetime.datetime.now(ZoneInfo("Europe/Berlin"))-datetime.timedelta(hours=1),#get the trains that are departing in +- 1 hour
        max_trips=max_numb_of_trains
    )
        self.trains = [Train(client_departures) for client_departures in train_info]
        for i in self.trains:
            i.print_to_file(name_of_file)
    def sort_by_ID(self):#sorts the trains by their ID this is used to find duplicates
        self.trains.sort(key=attrgetter('Train_ID'))
    
    def remove_duplicates(self):
        self.sort_by_ID()
        num_of_removed_duplicates = 0
        i = 0
        while(i < len(self.trains)-1):
            if(self.trains[i].Train_ID == "None"):
                break
            if(self.trains[i].Train_ID == self.trains[i+1].Train_ID):#if the ID of the current train is the same as the next one
                num_of_removed_duplicates += 1
                if(self.trains[i].delay > self.trains[i+1].delay):#remove the one with the lower delay, as this is the one that is not up to date(delays typically increase)
                    self.trains.pop(i+1)
                else:
                    self.trains.pop(i)
            else:
                i+=1
                
        print("Removed ",num_of_removed_duplicates," duplicates")
    
    def load_from_file(self,file_name):
        line=0
        while True:
            train = Train()
            train.get_train_info_from_file(file_name, line) 
        
            if(train.Train_ID == "None"):
                break
                print("There are ",len(self.trains)," trains in the list")
            self.trains.append(train)
            line+=1
        
    def replace_file(self,file_name):
        file = open(file_name,"w")
        file.close()
        file = open(file_name,"a")
        for i in self.trains:
            i.print_to_file(file_name)
            
        file.close()
             
def add_new_trains_to_file(max_num_of_new_trains):
    File_Mangagment = filemanagement(max_num_of_new_trains)
    File_Mangagment.load_from_file(name_of_file)
    File_Mangagment.sort_by_ID() 
    File_Mangagment.remove_duplicates()
    File_Mangagment.replace_file(name_of_file)
    print("There are" ,len(File_Mangagment.trains), "Trains to be found in the file.")  
while(True):    
    add_new_trains_to_file(100)
    import time
    from zoneinfo import ZoneInfo
    
    print("Updated the file")
    print(datetime.datetime.now(ZoneInfo("Europe/Berlin")))
    time.sleep(2*60) #sleep for 2 minutes such that the API is not overloaded




