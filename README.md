# HRI_Project
###HRI Project - Elective in AI

Inside this master branch you find all the files corresponding to "sample" directory of playgorund folder.

In order to use them, do the following steps

All actions have to be done from docker folder: 

./run_nginx.bash   //for the image pepper 


Then after executing the command ./run_bash 0.4.1:

run the naoqi server: 

1 - cd /opt/Aldebaran/naoqi..(use tab) \
2 - ./naoqi 

run the modim server: 

1-  cd /home/robot/src/modim/src/GUI/ \
2-  python ws_server.py -robot pepper

Go on the browser at the url: http://localhost/sample/index.html

run the modim client:

1-  cd playground/html/sample/scripts/ \
2-  python restaurant.py

the file restaurant.py contains at the moment a simple interaction where first of all pepper asks to select the language to a guest coming into the restaurant, and then it asks how many people they are, and depending on his answer a table for the corresponding number of people is assigned, and the table is marked as taken (not available) \ 
 
To run commands in ASR modality, another script is needed to be executed, and we have: \

cd src/pepper_tools/asr \
python human_say.py --sentence 'yes' \

-the last command with yes is an example-
