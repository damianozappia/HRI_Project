import sys
import time
import os
import random
import numpy as np

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

    # ---------------------
    # tables don't work because I don't know how to pass parameters to functions while using modim

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


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')


    mws.run_interaction(i2)


