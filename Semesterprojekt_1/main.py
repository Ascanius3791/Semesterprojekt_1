#!/usr/bin/env python3

from operator import attrgetter
import string
import datetime
from pyhafas import HafasClient
from pyhafas.profile import DBProfile

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
 
                  
class analysis:
    trains = []
    allowed_types = ["ICE","RE","S","U","STR","Bus","IC","RB","unknown"]
    
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
            if "ICE" == i.type_of_train:
                total_ICE +=1
                if(i.cancelled):
                    cancelled_ICE+=1
            if "RE" == i.type_of_train:
                total_RE +=1
                if(i.cancelled):
                    cancelled_RE+=1
            if "S" == i.type_of_train:
                total_S +=1
                if(i.cancelled):
                    cancelled_S+=1
            if "U" == i.type_of_train:
                total_U +=1
                if(i.cancelled):
                    cancelled_U+=1
            if "STR" == i.type_of_train:
                total_STR +=1
                if(i.cancelled):
                    cancelled_STR+=1
            if "Bus" == i.type_of_train:
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
    
    def delay_by_type(self,type_of_train):
        if(type_of_train not in self.allowed_types):
            print("Invalid type of train")
            return
        total_num_delay = 0
        total_trains = 0
        for i in self.trains:
            if i.type_of_train == type_of_train:
                total_trains += 1
                if(i.delay > 0):
                    total_num_delay += 1
        if(total_trains==0):
            print("No ",type_of_train," found")
            return       
        print("total delay of ",type_of_train,": ",total_num_delay/total_trains*100, "%")
        return total_num_delay/total_trains*100 
          
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
        if(total_trains == 0):
            return 0
        return total_delay/total_trains
        
    #now from here lets annswer the questions
    #1hat are the rush hours of the day, where the most trains depart?      
    
#print(client.locations("Frankfurt(Main)Hbf")[0].id) #example of how to access the info about the self.tation
#input("Press Enter to continue...\n\n")


analysis = analysis()
analysis.load_from_file(name_of_file)
analysis.trains[0].print()


analysis.cancellations_by_type()

analysis.average_delay_by_type("ICE")
analysis.average_delay_by_type("RE")
analysis.average_delay_by_type("S")
analysis.average_delay_by_type("U")
analysis.average_delay_by_type("STR")
analysis.average_delay_by_type("Bus")
analysis.average_delay_by_type("unknown")

analysis.delay_by_type("ICE")
analysis.delay_by_type("RE")
analysis.delay_by_type("S")
analysis.delay_by_type("U")
analysis.delay_by_type("STR")
analysis.delay_by_type("Bus")
analysis.delay_by_type("unknown")

