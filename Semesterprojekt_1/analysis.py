from operator import attrgetter
import string
import datetime
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from train_class import Train
#client = HafasClient(DBProfile())
#
# station_ID = client.locations("Frankfurt(Main)Hbf")[0].id

name_of_file = "/scratch/mesonqcd/hoffmann/ML/train_info.txt"
file = open(name_of_file,"a")

                  
class analysis:
    trains = []
    allowed_types = ["ICE","RE","S","U","STR","Bus","IC","RB","unknown"]
    
    def remove_unkown_and_Bus(self):
        self.trains = [i for i in self.trains if i.type_of_train != "unknown"]
        self.trains = [i for i in self.trains if i.type_of_train != "Bus"]
        print("There are ",len(self.trains)," trains in the list, unknown and Bus are removed")

    def remove_everything_but(self,type_of_train):
        if(type_of_train not in self.allowed_types):
            print("Invalid type of train")
            return
        self.trains = [i for i in self.trains if i.type_of_train == type_of_train]
        print("There are ",len(self.trains)," trains in the list")
        print("Only ",type_of_train," are left")

    def get_rush_hours(self,print_rush_hours = True):
        '''Returns a list of the number of trains departing in each hour of the day, also plots a bar chart of the data'''
        
        departure_times = [i.departure[10:16] for i in self.trains]
        
        departure_hours = [int(i[1:3]) for i in departure_times]
        
        rush_hours = [0]*24
        for i in departure_hours:
            rush_hours[i] += 1
        if(print_rush_hours):
            print("The rush hours are: ")
            for i in range(24):
                if(rush_hours[i] > 0):
                    print(i,"-",i+1,": ",rush_hours[i]," trains")

        plt.bar([i for i in range(24)],rush_hours,label='departure times',color="red")
        plt.legend()
        plt.xlabel('Hour')
        plt.xlim(-1,24)
        plt.ylabel('Number of trains')
        plt.xticks([i for i in range(24)])
        plt.title('Rush hours')
        plt.savefig('rush_hours.png')
        plt.show()
        plt.clf()
        return rush_hours
    
    def get_cancellation_rush_hours(self,print_rush_hours = True):
        '''Returns a list of the number of cancelled trains departing in each hour of the day, also plots a bar chart of the data'''
        
        departure_times = [i.departure[10:16] for i in self.trains if i.cancelled]
        #[print(i) for i in self.trains if i.cancelled]
        departure_hours = [int(i[1:3]) for i in departure_times]
        print(departure_hours)
        rush_hours = [0]*24
        for i in departure_hours:
            rush_hours[i] += 1
        if(print_rush_hours):
            print("The rush hours for cancellations are: ")
            for i in range(24):
                if(rush_hours[i] > 0):
                    print(i,"-",i+1,": ",rush_hours[i]," trains")
        plt.bar([i for i in range(24)],rush_hours,label='departure times',color="red")
        plt.legend()
        plt.xlabel('Hour')
        plt.ylabel('Number of cancelled trains')
        plt.xticks([i for i in range(24)])
        plt.title('Cancellation rush hours')
        plt.savefig('cancellation_rush_hours.png')
        plt.show()
        plt.clf()
        print("There are ",sum(rush_hours)," cancelled trains")
        return rush_hours

    def get_relative_cancellation_rush_hours(self):
        '''Returns a list of the number of cancelled trains, relative to the total number of trains, departing in each hour of the day, also plots a bar chart of the data'''
        normal_rush_hours = self.get_rush_hours(False)
        cancellation_rush_hours = self.get_cancellation_rush_hours(False)
        relative_cancellation_rush_hours = [0]*24
        for i in range(24):
            if(normal_rush_hours[i] != 0):
                relative_cancellation_rush_hours[i] = cancellation_rush_hours[i]/normal_rush_hours[i]
        print("The relative rush hours for cancellations are: ")
        for i in range(24):
            if(relative_cancellation_rush_hours[i] > 0):
                print(i,"-",i+1,": ",relative_cancellation_rush_hours[i]*100,"%")
        plt.bar([i for i in range(24)],relative_cancellation_rush_hours,label='departure times')
        plt.legend()
        plt.xlabel('Hour')
        plt.ylabel('Percentage of cancelled trains')
        plt.xticks([i for i in range(24)])
        plt.title('Relative cancellation rush hours')
        plt.savefig('relative_cancellation_rush_hours.png')
        plt.show()
        plt.clf()
        return relative_cancellation_rush_hours

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
    def delay_average_per_hour(self):

        delays=[]


        for j in range(24):
         tmp=[]
         for i in self.trains:
             index=int(i.departure[11:13])
             if index==j:
               tmp.append(i.delay)
               #print("index",index)
         mean=np.sum(tmp)
             

         delays.append(mean)
             #print("delay",delays[0])
        print(len(delays))
        delays=np.array(delays)
        print(delays)
        return delays

          
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

    def get_train_density_per_hour(self):
        '''Returns a list of the number of trains departing in each hour of the day, also plots a bar chart of the data'''
        
        departure_times = [i.departure[10:16] for i in self.trains]
        
        departure_hours = [int(i[1:3]) for i in departure_times]
        
        rush_hours = [0]*24
        for i in departure_hours:
            rush_hours[i] += 1
        print("The rush hours are: ",rush_hours)
        
        return rush_hours  
    

    #get correlation  matrix for delay and density to check correlation between these two stochastic variables 

    def get_covariance(self,delay,density):
        delay=np.array(delay)
        density=np.array(density)
        print(delay,density)
        cov=np.corrcoef(delay,density)
        print(cov.shape)
        print("covariance",cov)
        #now plot correlation matrix as function of average delay in minutes and density inetgrated over 10 minutes 

        Delay,Density=np.meshgrid(delay,density)
        Corr=np.cov(Delay,Density)

        trace=np.trace(cov)
        #Corr.reshape(24,24)

        print("total cross correlation is",trace)
        
        plt.scatter(density,delay,color="black")
        plt.xlabel("Train density")
        plt.ylabel("Delay in minutes")
        plt.xticks([50,100,150,200,250,300])
        ax=plt.gca()
        ax.minorticks_on()
        plt.savefig("Correlation_Delay_number.png")

        plt.show()

  
    def probability_delay(self):

        #sort trains according to departure 

        departure_time=[float(i.departure[11:13])*60.0+float(i.departure[14:16]) for i in self.trains]
        #departure_hours = [int(i[1:3]) for i in departure_time]


        sorted_indices=np.argsort(departure_time)

        self.trains=np.array(self.trains)

        Trains=self.trains[sorted_indices]
        for i in sorted_indices:
            print(departure_time[i],Trains[i])

        print(departure_time)

        Ntrains=100 #trains after delay 
        
        nexttrains=[]
        num_delay=0
        for i in range(len(Trains)):
           if Trains[i].delay>0.0:
               num_delay+=1
               print("delay number",num_delay)
               nexttrains.append(Trains[i:i+100])
               i+=Ntrains
           print("iter",i)
        print(len(nexttrains[1]))

        averagedelays=[]
        for elem in nexttrains:
            tmp=[]
            num_delays=0
            for elem2 in elem:
                if elem2.delay>0:
                    num_delays+=1
            averagedelays.append(num_delays)

        averagedelays=np.array(averagedelays)
        print(averagedelays/100)            
        #nexttrains=np.array(nexttrains)  
        print(np.mean(averagedelays/100)) 
        return None


             





    #now from here lets annswer the questions
    #1hat are the rush hours of the day, where the most trains depart?      
    
#print(client.locations("Frankfurt(Main)Hbf")[0].id) #example of how to access the info about the self.station
#input("Press Enter to continue...\n\n")


analysis = analysis()
analysis.load_from_file(name_of_file)

#analysis.get_rush_hours()

#analysis.get_cancellation_rush_hours()

#number=analysis.get_train_density_per_hour()
#delay=analysis.delay_average_per_hour()
#analysis.get_covariance(delay,number)

#analysis.get_relative_cancellation_rush_hours()
analysis.probability_delay()