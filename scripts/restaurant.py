import sys
import argparse
import time
import datetime
import os
import csv
import random
import numpy as np
import io
from collections import deque

#tables matrix for the seats 
tables = np.ones((2,3), dtype = 'bool')
language = ''

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print ("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

# Set MODIM_IP to connnect to remote MODIM server

import ws_client
from ws_client import *
import qi

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

def add_to_order(x):
    f = open("menu.txt", "a")
    f.write(x)
    f.close()
    

def welcome():
    global tts_service
    global language
    tables_cap = [2, 4, 2, 2, 5]

    im.init()

    im.ask('welcome')

    q = ('language')
    a = im.ask(q)

    
    if(a == 'italiano'):
        im.setProfile(['*', '*', 'it', '*'])
    elif(a == 'spanish'):
        im.setProfile(['*', '*', 'es', '*'])
    elif(a == 'english'):
        im.setProfile(['*', '*', 'en', '*'])

    im.execute(a)

    q = ('people')
    a = im.ask(q)

    if(a == 'one'):
        num_clients = 1
    elif(a == 'two'):
        num_clients = 2
    elif(a == 'three'):
        num_clients = 3
    elif(a == 'four'):
        num_clients = 4

    indexes = []
    for index, cap in enumerate(tables_cap):
        if cap >= num_clients:
            indexes.append(index)

    table_available = False
    for index in indexes:
        with open('/home/robot/playground/html/sample/logs/table_'+str(index+1)+'.csv', "r") as csvFile:
            line = csvFile.readline()
            while line:
                lastline = line
                line = csvFile.readline()
        csvFile.close()
        numclients = lastline.split(',')[0]
        if int(numclients) is 0:
            table_available = True
            im.execute(a)
    if not table_available:
        im.execute('full')    
    
    if (a!='timeout'):
        im.execute('wait_for_ordination')

    im.init()


def menu():

    im.init()
    #im.execute('action1')

    a = im.executeModality('TEXT_default','Are your ready to order?')
    im.executeModality('ASR',['yes','no'])
    
    #now we wait for answer
    a = im.ask(actionname=None, timeout=20)

    while(a != 'yes'):
      a = im.executeModality('TEXT_default','Ok, I will wait then..')
      time.sleep(5)
      #ask again if guests are ready
      a = im.executeModality('TEXT_default','Are your ready to order?')
      im.executeModality('ASR',['yes','no'])
      a = im.ask(actionname=None, timeout=10)
    
    table_num = im.ask('table_confirmation', timeout=20)
    print("-------------------------------------------")
    print("the table number is", table_num)
    print("-------------------------------------------")

    #--------------
    menu_flag = True
    dishes_ordered = ""
    while(menu_flag):
      
        b = im.ask('menu', timeout=10)
        im.execute(b)
        dishes_ordered = dishes_ordered + b + ", "

        b = im.executeModality('TEXT_default','Is it ok? do you want something else?')
        im.executeModality('ASR',['yes','no'])
        #now we wait for answer
        b = im.ask(actionname=None, timeout=10)

        if b != "no":
            b = im.executeModality('TEXT_default','great, tell me..')
            time.sleep(1)
        else:
            menu_flag = False

    with open('/home/robot/playground/html/sample/logs/table_'+str(table_num)+'.csv', 'a') as csvFile:
        csvFile.writelines(unicode(dishes_ordered+"\n"))
    csvFile.close()
     
    time.sleep(2)
    #-------------------------
   
    if (b!='timeout'):
        #im.execute(b)
        im.execute('order_confirmed')


    im.init()


def info():
    im.init()
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

attended_clients = 1
client_queue =  deque()
touchstatus = { }
def onTouched(value):
    global touchstatus
    global client_queue
    global attended_clients
    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])
            if p[0] == 'Head':
                client_queue.append(attended_clients)
                attended_clients += 1
                sentence = "I noticed you, please be patient, your turn is the number "+str(attended_clients)
                tts_service.say(sentence)
                print("-------------------------------------------")
                print ("  -- Say: "+sentence)
                print("-------------------------------------------")
        touchstatus[p[0]] = p[1]

if __name__ == "__main__":
    # global tts_service
    # global client_queue
    # global attended_clients

    client_queue.append(attended_clients)


    parser = argparse.ArgumentParser()

    init_tables()

    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--speed", type=int, default=100,
                        help="speed")
    

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    speed = args.speed

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["ReactToTouch", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)


    app.start()
    session = app.session

    #Starting services
    memory_service  = session.service("ALMemory")
    tts_service = session.service("ALTextToSpeech")
    touch_service = session.service("ALTouch")

    tts_service.setLanguage("English")
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)

    #subscribe to any change on any touch sensor
    anyTouch = memory_service.subscriber("TouchChanged")
    idAnyTouch = anyTouch.signal.connect(onTouched)

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    try:
        while len(client_queue) > 0:
            #mws.run_interaction(welcome)
            next_turn = client_queue.popleft()
            if len(client_queue) > 0:
                sentence = "Calling to client with number "+str(next_turn)
                tts_service.say(sentence)
                print("-------------------------------------------")
                print ("  -- Say: "+sentence)
                print("-------------------------------------------")
            #mws.run_interaction(info)
            mws.run_interaction(menu)

    except KeyboardInterrupt:
         #Disconnecting callbacks and Threads
        anyTouch.signal.disconnect(idAnyTouch)
        print("Interaction finished")
        sys.exit(1)