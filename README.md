# ICT-Turtlebot-Project
Network:

	if you are using the UNISA network to test the program you might switch your IP:
	
	1 $ nano ~/.bashrc 
	into the last two line  switch the ip as
	2 export ROS_MASTER_URI=http://localhost:11311
	3 export ROS_HOSTNAME=localhost
	optional command for export the turtlebot waffle it will automatically export the turtlebot before you launch the world
	4 export TURTLEBOT3_MODEL=waffle	
	
	save and exit the text editor
	
	$ source ~/.bashrc 

Set up enviorment

	1. Install python Open CV
		$ sudo apt update
		$ sudo apt install python3-pip
		$ pip install opencv-python


	2. My_ground_plane  folder need to be move into ~/.gazebo/models

	In terminal
	3. $ chmod +x python file

	4. you might need a dos2unix on obstacle python file

		$ sudo apt-get install dos2unix
		$ dos2unix pythonfile.py
 
#Starting the simulator

In terminal:
	
	(optional if you followed the Network part )	
	1. export TURTLEBOT3_MODEL=waffle 


	launch the simulator world
	2. roslaunch project projectworld.launch

	launch the python file
	3. roslaunch project Combine.launch

# Reopen the simulator

	In terminal
		$ killall gzcleint
		$ killall gzsever
		$ roslaunch project projectworld.launch
