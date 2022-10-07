from threading import Thread
import os
import time
from queue import Queue




global a
a = 0
#q.put(a)

mobile_counter_customer = []



clear = lambda: os. system('cls')
class Counter:
      def __init__(self,counter_id):
        self.counter_id = counter_id
        #self.length = 0
        self.queue = []
        self.OF = 0.0
        self.output = 0                 # number of cust exiting counter in interval of five minutes
        self.weightage = 0


class Customer:
  def __init__(self,customer_id):  #instance of the class counter
    self.customer_id = customer_id
    self.counter = 0

global total_counters    
total_counters = []

global open_counters
open_counters = []   #array of counter class instances

global closed_counters
closed_counters = []  #array of counter class instances

global cutomer_list
customer_list = dict()



max_length = int(input("Enter maximum length for each counter:\n"))
num_counter = int(input("Enter number of counters:\n"))

threshold = max_length//2


counters= dict()  #key: value :: counter_name: counter_class

for i in range(num_counter): 
    counter_num = "counter_%d" % (i+1)
    counters[counter_num] = Counter(i+1)
    closed_counters.append(counters[counter_num])



def Weightage(Counter_input):
    if len(Counter_input.queue) != 0:                                      # if counter has customers in it
        Counter_input.weightage = Counter_input.OF/(len(Counter_input.queue)) 
    else:                                                                  # if counter has no customers in it
        Counter_input.weightage = 0

def Entry(customer):
  if open_counters== []:                                                  # first customer condition
    open_counters.append(closed_counters.pop(0))
    open_counters[-1].queue.append(customer.customer_id)
    customer.counter = open_counters[-1].counter_id
    
    print("customer" + str(customer.customer_id) +  " is assigned to counter: " + str(open_counters[-1].counter_id))
    
  else: 

    potential = -1
    c = 0                                                                                          # to check later how many counters are above threshold
    for item in open_counters:

      if len(item.queue) < threshold:
        c = 1
        if(item.weightage>potential):
          potential = item.weightage                                                              # Finding that node that holds the largest weightage
          potential_data = item
    
    if c == 1:                                                                                    # if there is a counter with less than threshold customers
      customer.counter = potential_data.counter_id                                                  # assign that counter to customer
      potential_data.queue.append(customer.customer_id)                                                         # add customer to that counter's queue
      print ("customer" + str(customer.customer_id) +  " is assigned to counter:", potential_data.counter_id)
      Weightage(potential_data)                                                                    # update weightage of that counter

    elif c==0:                                                                                    # all open counters have reached threshold length
          if closed_counters!=[]:                                                                 # all open > threshold AND closed counters EXIST
                open_counters.append(closed_counters.pop(0))  
                customer.counter = open_counters[-1].counter_id
                open_counters[-1].queue.append(customer.customer_id)                              # add customer to that counter's queue'
                print("customer" + str(customer.customer_id) + " is assigned to counter:", open_counters[-1].counter_id)
                Weightage(open_counters[-1])
            
          else:                                                                                   # all open > threshold AND NO closed counters exist 
                max_weightage_allOpen_allAboveThreshold = -1
                z = 0
                for i in open_counters:
                      
                      #print(i.weightage)
                      if i.weightage > max_weightage_allOpen_allAboveThreshold and len(i.queue) < max_length:       # finding the counter with the largest weightage and counter is not full
                           
                            z = 1
                            max_weightage_allOpen_allAboveThreshold = i.weightage
                            max_weightage_allOpen_allAboveThreshold_data = i
            
                if z==1:                                                                            # at least one counter which is not FULL
                      customer.counter = max_weightage_allOpen_allAboveThreshold_data.counter_id
                      max_weightage_allOpen_allAboveThreshold_data.queue.append(customer.customer_id)
                      print("customer" + str(customer.customer_id) +  " is assigned to counter:" , max_weightage_allOpen_allAboveThreshold_data.counter_id)
                      Weightage(max_weightage_allOpen_allAboveThreshold_data)
                else:                                                                               # all counters are open and full
                      print("OPEN MOBILE COUNTERS")
                      mobile_counter_customer.append(customer)
                      customer.counter = -1                                                         # -1 indicates mobile counters
                     

  customer_list.update({customer.customer_id:[customer, customer.counter]})
    

      
def Exit(customer):
    counter_of_exit_id = customer.counter                                                   #find "id" of the counter from which customer exits
    if customer.customer_id == counters["counter_%d" % counter_of_exit_id].queue[0]:
          
      print("customer " , customer.customer_id,  "exited from counter ", counter_of_exit_id)
      
      counters["counter_%d" % counter_of_exit_id].queue.pop(0)                                       #remove customer from that counter's queue **************************
      customer.counter = 0                                                                          #remove customer: counter relationship
      
      if (len((counters["counter_%d" % counter_of_exit_id]).queue) == 0):
          closed_counters.append(open_counters.pop(open_counters.index(counters["counter_%d" % counter_of_exit_id])))
          
          closed_counters[-1].OF = 0
          
      else:
          
          counters["counter_%d" % counter_of_exit_id].output += 1
      
      customer_list.pop(customer.customer_id)
      Weightage(counters["counter_%d" % counter_of_exit_id])
    
    else:
          print("Invalid Exit\n\n")

def main(threadname,q):
    cont = 0
    
    while(cont==0):
        
          
        a = int(input("Enter \n 1.Entry \n 2.Exit \n 3.Exit Program \n"))
        if(a==1):
            b = int(input("Enter customer id:\n"))
            if b not in customer_list.keys():
              Entry(Customer(b))
              
            else:
              print("Customer", b, "already present in counter: ", customer_list[b][1])
        elif(a==2):
            b = int(input("Enter customer id:\n"))
            Exit(customer_list[b][0])
        elif(a==3):
            q.put(a)
            exit()
        for i in open_counters:
            #print("Counter:", i.counter_id, " has ", (i.queue))
            #print()
            """for i in closed_counters:
            print("Counter:", i.counter_id, " has ", (i.queue))
            print()"""
        #print(customer_list)
        print()
        for i, values in counters.items():
            
            print(i, ":", values.queue) 


def os_of_calculator(threadname,q):
    
    while(True):
        a = q.get()
        if a==3:
            quit()
        
        time.sleep(5)

        for i in open_counters:
            i.OF = i.output / 2             # calculate OF for a every open counter
            i.output = 0
            #print(i.counter_id, i.OF)
            #print()
            
    
    
    
    

q=Queue()
abc = Thread(target = main,args=("thread1",q))


bcd = Thread(target = os_of_calculator,args=("thread2",q))

abc.start()
bcd.start()
abc.join()
bcd.join()


