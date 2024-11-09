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
        try:
            self.Train_ID = self.Train_ID.replace(" ","")
            self.destination = self.destination.replace(" ","")
            self.name = self.name.replace(" ","")
            self.platform = self.platform.replace(" ","")
        except:
            pass
        file = open(file_name,"a")
        #remove the " " from the ID this is needed to make it consistent, else there are "random" amounts of " " in the ID, same goes for the destination
        
        file.write(str(self.Train_ID) + " ")
        file.write(str(self.departure) + " ")
        file.write(str(self.delay) + " ")
        file.write(str(self.cancelled) + " ")
        
        file.write(str(self.destination) + " ")
        file.write(str(self.type_of_train) + " ")
        
        file.write(str(self.name) + " ")
        
        file.write(str(self.platform) + " ")
        file.write("\n")
        
        file.close()

      
    def get_train_info_from_file(self,file_name,line):
        file = open(file_name,"r")
        
        for _ in range(line):
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