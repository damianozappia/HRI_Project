# HRI_Project
## HRI Project - Elective in AI

Inside this master branch you find all the files corresponding to "sample" directory of playgorund folder.

In order to use them, do the following steps

All actions have to be done from docker folder:

### Run Web Server
In order to see a simulation of the table of the pepper robot

    cd HRI/doker
    sudo ./run_nginx.bash

### Run Docker

    cd HRI/doker
    sudo ./run.bash 0.4.1

For special access to the features of the robot pepper use naoqui server:

    cd /opt/Aldebaran/naoqi..(use tab)
    ./naoqi 

Inside the docker we have access to the modim server:

    cd ~/src/modim/src/GUI/
    python ws_server.py -robot pepper

Go on the browser at the url: http://localhost/sample/index.html

Run the modim client main code:

    cd ~/playground/html/sample/scripts/
    python restaurant.py



the file restaurant.py contains at the moment a simple interaction where first of all pepper asks to select the language to a guest coming into the restaurant, and then it asks how many people they are, and depending on his answer a table for the corresponding number of people is assigned, and the table is marked as taken (not available) \ 

### Interactions outside the tablet
Execution through commands in ASR modality (keyboard interaction)

#### Speech recognition 
To interact with the robot using speech is needed to call ASR script:
 
To run commands in ASR modality, another script is needed to be executed, and we have: 

    cd HRI/doker
    sudo ./run_bash 0.4.1

    cd src/pepper_tools/asr
    python human_say.py --sentence 'yes' 

-the last command with yes is an example-

#### Touch robot body 
To interact with the robot by activating the sensors in its body:

    cd HRI/doker
    sudo ./run_bash 0.4.1

    cd src/pepper_tools/touch
    python touch_sim.py

This will generate a touch in the head and in the hands, currently in the project is only relevant the touch in the head, therefore all the others will be ignored.
