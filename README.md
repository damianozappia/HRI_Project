# HRI_Project
HRI Project - Elective in AI
Inside this master branch you find all the files corresponding to "sample" directory of playgorund folder.

In order to use them, do the following steps

All actions have to be done from docker folder:

./run_nginx.bash   //for the image pepper 

run the naoqi server: 
1 - cd /opt/Aldebaran/naoqi..(use tab)
2 - ./naoqi 

run the modim server: 
--
1-  cd /home/robot/src/modim/src/GUI/
2-  python ws_server.py -robot pepper 
--

run the modim client:
1-  cd playground/html/sample/scripts/
1-  python restaurant.py

the file restaurant.py contains at the moment a siample interaction where a to guest coming to the restaurant is asked how many people they are, and depending on his answer a table for the corresponding number of people is assigned  
