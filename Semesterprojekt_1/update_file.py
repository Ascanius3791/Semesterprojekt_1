#!/usr/bin/env python3

from operator import attrgetter
import string
import datetime
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
import time
from zoneinfo import ZoneInfo
from train_class import Train

client = HafasClient(DBProfile())
station_ID = client.locations("Frankfurt(Main)Hbf")[0].id
name_of_file = "train_info.txt"
file = open(name_of_file,"a")

       
class filemanagement:
    trains = []

    def __init__(self,max_numb_of_trains):
        train_info = []
        got_info = False
        while(not got_info and max_numb_of_trains > 0):
            try:
                train_info = client.departures(
                station=station_ID,
                duration=120,
                date=datetime.datetime.now(ZoneInfo("Europe/Berlin"))-datetime.timedelta(hours=1),#get the trains that are departing in +- 1 hour
                max_trips=max_numb_of_trains
                
            )
                got_info = True
            except:
                print("Could not load all the trains, trying again with 2/3 of the trains")
                max_numb_of_trains = int(max_numb_of_trains*2/3)
                time.sleep(1)
        if(max_numb_of_trains == 0):
            print("Could not load the trains")
            return
        
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