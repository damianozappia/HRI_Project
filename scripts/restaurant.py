import sys
import argparse
import time
import datetime
import os
import csv
import random
import numpy as np
import io



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
    
    table_num = im.ask('table_confirmation', timeout=10)
    print("-------------------------------------------")
    print("the table number issssss", table_num)
    print("-------------------------------------------")

    #--------------
    menu_flag = True
    dishes_ordered = ""
    while(menu_flag):
      
        b = im.ask('menu', timeout=10)
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
        im.execute('goodbye')


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


touchstatus = { }
language = 'english'

def onTouched(value):
    global touchstatus
    global language
    print ("Touch value=",value)

    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])
            if p[0] == 'Head':
                tts_service.say("I noticed you please be patient")
                print("-------------------------------------------")
                print ("  -- Say: "+"I noticed you please be patient")
                print("-------------------------------------------")
        touchstatus[p[0]] = p[1]

if __name__ == "__main__":
    # global tts_service
    # global client_queue
    # global attended_clients


if __name__ == "__main__":
    global tts_service
    parser = argparse.ArgumentParser()

    tables = "1 1 1 1 1 1"
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
    strsay = args.sentence
    language = args.language
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

    tts_service.setLanguage(language)
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
        while True:
            #mws.run_interaction(welcome)
                tts_service.say(sentence)
                print("-------------------------------------------")
                print ("  -- Say: "+sentence)
                print("-------------------------------------------")
            #mws.run_interaction(menu)
            mws.run_interaction(info)
    except KeyboardInterrupt:
         #Disconnecting callbacks and Threads
        anyTouch.signal.disconnect(idAnyTouch)
        print("Interaction finished")
        sys.exit(1)