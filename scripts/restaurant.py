import sys
import time
import os
import random

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    sys.exit(1)

# Set MODIM_IP to connnect to remote MODIM server

import ws_client
from ws_client import *

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

    print("-------------------------------")
    print("the A IS: ", a)
    print("-------------------------------")
    #print("THE TYPE OF a IS ", type(a))
    
    if(a.find('italian') != -1):
        im.setProfile(['*', '*', 'it', '*'])
# spanish doesn't work because the option is not present by system (we have to see how to fix)
    elif(a.find('spanish') != -1):
        im.setProfile(['*', '*', 'es', '*'])
    elif(a.find('english') != -1):
        im.setProfile(['*', '*', 'en', '*'])


    im.execute(a)

    q = ('people')
    
    a = im.ask(q)
    
    if (a!='timeout'):
        im.execute(a)
        im.execute('see_you')

    im.init()


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(i2)


