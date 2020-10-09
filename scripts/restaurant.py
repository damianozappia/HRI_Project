import sys
import time
import datetime
import os
import csv
import random
import numpy as np
import io

#tables matrix for the seats 
tables = np.ones((2,3), dtype = 'bool')

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    sys.exit(1)

# Set MODIM_IP to connnect to remote MODIM server

import ws_client
from ws_client import *

def init_tables():
    nowTime = datetime.datetime.now()

    for table_num in range(1,6):
        with io.open('/home/robot/playground/html/sample/logs/table_'+str(table_num)+'.csv', 'w') as csvFile:
            csvFile.writelines(unicode('0,'+str(nowTime)+"\n"))
        csvFile.close()

def is_table_free(table_num):
    with io.open('/home/robot/playground/html/sample/logs/table_'+str(table_num)+'.csv', "r") as csvFile:
        line = csvFile.readline()
        while line:
            lastline = line
            line = csvFile.readline()
    csvFile.close()
    numclients = lastline.split(',')[0]
    return int(numclients) == 0

def write_table(table_num, val):
    with io.open('/home/robot/playground/html/sample/logs/table_'+str(table_num)+'.csv', 'a') as csvFile:
        csvFile.writelines(unicode('val,'+str(nowTime)+"\n"))
    csvFile.close()

def register_customer():
    pass

def customer_payment():
    pass


def i1():

    im.init()

    im.ask('welcome')  # wait for button

    q = random.choice(['animal','color'])

    a = im.ask(q)

    if (a!='timeout'):
        im.execute(a)
        im.execute('goodbye')

    im.init()

def i2():

    im.init()

    im.ask('welcome')

    q = ('language')
    a = im.ask(q)

    
    if(a == 'italiano'):
        im.setProfile(['*', '*', 'it', '*'])
    # spanish doesn't work because the option is not present by system (we have to see how to fix)
    elif(a == 'spanish'):
        im.setProfile(['*', '*', 'es', '*'])
    elif(a == 'english'):
        im.setProfile(['*', '*', 'en', '*'])

    im.execute(a)

    
    q = ('people')
    a = im.ask(q)

    if(a == 'one'):
        if(tables[0][0] == True):
            tables[0][0] = False
            im.execute(a)
        else:
            im.execute('full')

    if(a == 'two'):
        if(tables[0][1] == True):
            tables[0][1] = False
            im.execute(a)
        else:
            im.execute('full')

    if(a == 'tree'):
        if(tables[0][2] == True):
            tables[0][2] = False
            im.execute(a)
        else:
            im.execute('full')
    
    
    if (a!='timeout'):
        im.execute('see_you')

    im.init()


def menu():

    im.init()
    #im.execute('action1')

    a = im.executeModality('TEXT_default','Are your ready to order?')
    im.executeModality('ASR',['yes','no'])
    
    #now we wait for answer
    a = im.ask(actionname=None, timeout=10)

    while(a != 'yes'):
      a = im.executeModality('TEXT_default','Ok, I will wait then..')
      time.sleep(5)
      #ask again if guests are ready
      a = im.executeModality('TEXT_default','Are your ready to order?')
      im.executeModality('ASR',['yes','no'])
      a = im.ask(actionname=None, timeout=10)
    
    a = im.ask('menu', timeout=10)

    if (a!='timeout'):
        im.execute(a)



    #--------------
    b = im.executeModality('TEXT_default','Is it ok? do you want something else?')
    im.executeModality('ASR',['yes','no'])

    while(b != "no"):
      b = im.executeModality('TEXT_default','great, tell me..')
      time.sleep(1)

      b = im.ask('menu', timeout=10)

      b = im.executeModality('TEXT_default','Is it ok? do you want something else?')
      im.executeModality('ASR',['yes','no'])
      
      #now we wait for answer
      b = im.ask(actionname=None, timeout=10)
     
    time.sleep(3)
    #-------------------------
   
    if (b!='timeout'):
        #im.execute(b)
        im.execute('goodbye')


    im.init()



def info():

    im.init()

    tables = ['Putooooo', 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH']
    print("=======================================================")
    print(tables)
    print("=======================================================")


    a = im.ask('info')

    if (a!='timeout'):
        im.execute(a)
    else:
        im.execute('goodbye')

    #if info are requested we start asking what guests need to know
    if (a == 'start'):
        a = im.ask('info_2')
    # then if the time is not over, we execute the action related to the requested info
    if (a!='timeout'):
        im.execute(a)
        im.execute('goodbye')

    im.init()


    



if __name__ == "__main__":
    tables = "1 1 1 1 1 1"
    init_tables()

    mws = ModimWSClient()
    # f = open("/home/robot/playground/html/sample/logs/tables.txt","w")
    # f.write(tables)
    # f.close()


    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')


    #mws.run_interaction(i2)
    mws.run_interaction(menu)
    #mws.run_interaction(info)
