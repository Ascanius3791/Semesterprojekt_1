#!/usr/bin/env python3

from operator import attrgetter
import string
import datetime
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
import matplotlib.pyplot as plt
import numpy as np

from train_class import Train
#client = HafasClient(DBProfile())
#
# station_ID = client.locations("Frankfurt(Main)Hbf")[0].id

name_of_file = "train_info.txt"
file = open(name_of_file,"a")

                  
class analysis:
    trains = []
    allowed_types = ["ICE","RE","S","U","STR","Bus","IC","RB","unknown"]
    
    def __init__(self):
        self.trains = []
        self.load_from_file(name_of_file)
        self.keep_only_ICE_RE_S_RB_IC()

    def remove_unkown_and_Bus(self):
        self.trains = [i for i in self.trains if i.type_of_train != "unknown"]
        self.trains = [i for i in self.trains if i.type_of_train != "Bus"]
        print("There are ",len(self.trains)," trains in the list, unknown and Bus are removed")

    def keep_only_ICE_RE_S_RB_IC(self):
        self.trains = [i for i in self.trains if i.type_of_train in ["ICE","RE","S","RB","IC"]]
        print("There are ",len(self.trains)," trains in the list")
        print("Only ICE, RE, S, RB and IC are left")

    def remove_everything_but(self,type_of_train):
        if(type_of_train not in self.allowed_types):
            print("Invalid type of train")
            return
        self.trains = [i for i in self.trains if i.type_of_train == type_of_train]
        print("There are ",len(self.trains)," trains in the list")
        print("Only ",type_of_train," are left")

    def keep_only(self,type_of_train):
        if(type_of_train not in self.allowed_types):
            print("Invalid type of train")
            return
        self.trains = [i for i in self.trains if i.type_of_train is not type_of_train]
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

        plt.bar([i for i in range(24)],rush_hours,label='departure times')
        plt.legend()
        plt.xlabel('Hour')
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
            plt.bar([i for i in range(24)],rush_hours,label='departure times')
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
        print("The rush hours are: ")
        
        return rush_hours  
    
    def get_delay_distribution(self,print_delays = True, for_type = "all"):
        relevant_trains = self.trains
        if(for_type != "all"):
            if(for_type not in self.allowed_types):
                print("Invalid type of train")
                return
        if(for_type != "all"):
            relevant_trains = [i for i in self.trains if i.type_of_train == for_type]
        delays = [i.delay for i in relevant_trains] #filter out all but selected type of train at will
        #delays.sort()
        #5 min intervals
        max_delay = max(delays)
        delay_distribution = [0]*int((max_delay)/5+1)
        for i in delays:
            delay_distribution[int((i)/5)] += 1
        if(print_delays):

            print("The delay distribution is: ")
            for i in range(len(delay_distribution)):
                if(delay_distribution[i] > 0):
                    print(i*5,"-",i*5+5,": ",delay_distribution[i]," trains")
            plt.bar([i*5 for i in range(len(delay_distribution))],delay_distribution,label='delays')
            plt.legend()
            plt.xlabel('Delay')
            plt.ylabel('log(Number of trains)')
            plt.yscale('log')
            plt.title('Delay distribution')
            plt.savefig('delay_distribution.png')
            plt.show()
            plt.clf()
        return delay_distribution

    def compare_delay_distrib(self):
        suburban = self.get_delay_distribution(False,"S")
        regional_RE = self.get_delay_distribution(False,"RE")
        regional_RB = self.get_delay_distribution(False,"RB")
        intercity_IC = self.get_delay_distribution(False,"IC")
        intercity_ICE = self.get_delay_distribution(False,"ICE")
        #unify the lengths
        max_len = max(len(suburban),len(regional_RE),len(regional_RB),len(intercity_IC),len(intercity_ICE))
        suburban += [0]*(max_len-len(suburban))
        regional_RE += [0]*(max_len-len(regional_RE))
        regional_RB += [0]*(max_len-len(regional_RB))
        intercity_IC += [0]*(max_len-len(intercity_IC))
        intercity_ICE += [0]*(max_len-len(intercity_ICE))
        #add RB and RE, and IC and ICE
        regional = [regional_RE[i]+regional_RB[i] for i in range(max_len)]
        intercity = [intercity_IC[i]+intercity_ICE[i] for i in range(max_len)]
        #plot the data
        x = [i * 5 for i in range(max_len)]

        # Width for each bar
        width = 1.2  # Adjust width as needed

        # Plot each dataset with an offset
        plt.bar([pos - width for pos in x], suburban, width, label='S')
        plt.bar(x, regional, width, label='RE+RB')
        plt.bar([pos + width for pos in x], intercity, width, label='IC+ICE')
        plt.legend()
        plt.xlabel('Delay')
        plt.yscale('log')
        plt.ylabel('log(Number of trains)')
        plt.title('Delay distribution by type of train')
        plt.savefig('delay_distribution_by_type.png')
        plt.show()
        plt.clf()
        return suburban,regional,intercity

    def get_cancellation_distribution(self,print_cancellations = True, for_type = "all"):
        relevant_trains = self.trains
        if(for_type != "all"):
            if(for_type not in self.allowed_types):
                print("Invalid type of train")
                return
        if(for_type != "all"):
            relevant_trains = [i for i in self.trains if i.type_of_train == for_type]
        cancellations = [i.cancelled for i in relevant_trains]
        cancellation_distribution = [0,0]
        for i in cancellations:
            if(i):
                cancellation_distribution[1] += 1
            else:
                cancellation_distribution[0] += 1

        cancellation_distribution[1] = cancellation_distribution[1]/len(relevant_trains)*100
        cancellation_distribution[0] = 100-cancellation_distribution[1]
        if(print_cancellations):
            print("The cancellation distribution is: ")
            print("Not cancelled: ",cancellation_distribution[0]," trains")
            print("Cancelled: ",cancellation_distribution[1]," trains")
            plt.bar(["Not cancelled","Cancelled"],cancellation_distribution,label='cancellations')
            plt.legend()
            plt.ylabel('Percentage of trains')
            plt.title('Cancellation distribution')
            plt.savefig('cancellation_distribution.png')
            plt.show()
            plt.clf()
        return cancellation_distribution
    
    def compare_cancellation_distrib(self):
        all_cancellations = self.get_cancellation_distribution(False)
        suburban = self.get_cancellation_distribution(False,"S")
        regional_RE = self.get_cancellation_distribution(False,"RE")
        regional_RB = self.get_cancellation_distribution(False,"RB")
        intercity_IC = self.get_cancellation_distribution(False,"IC")
        intercity_ICE = self.get_cancellation_distribution(False,"ICE")
        #unify the lengths
        max_len = 2
        #add RB and RE, and IC and ICE
        regional = [regional_RE[i]/2+regional_RB[i]/2 for i in range(2)]
        intercity = [intercity_IC[i]/2+intercity_ICE[i]/2 for i in range(2)]
        #plot the data
        x = [0,1]

        # Width for each bar
        width = 1.2*3/4

        # Plot zero component of cancellations only, also far all trains
        plt.bar(0-width, all_cancellations[1], width/4*2, label='All')
        plt.bar(0-width/3, suburban[1], width/4*2, label='S')
        plt.bar(0+width/3, regional[1], width/4*2, label='RE+RB')
        plt.bar(0+width, intercity[1], width/4*2, label='IC+ICE')
        plt.legend()
        plt.ylabel('Percentage of trains')
        plt.xticks([0],["Cancelled"])
        plt.title('Cancellation distribution by type of train')
        plt.savefig('cancellation_distribution_by_type.png')
        plt.show()
        plt.clf()
        return all_cancellations,suburban,regional,intercity

    #now from here lets annswer the questions
    #1hat are the rush hours of the day, where the most trains depart?      
    
#print(client.locations("Frankfurt(Main)Hbf")[0].id) #example of how to access the info about the self.station
#input("Press Enter to continue...\n\n")


analysis = analysis()

analysis.get_rush_hours()

analysis.get_cancellation_rush_hours()

analysis.get_relative_cancellation_rush_hours()

analysis.get_delay_distribution()
analysis.compare_delay_distrib()
analysis.get_cancellation_distribution()
analysis.compare_cancellation_distrib()

