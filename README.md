ICT-Turtlebot-Project

Git link:https://github.com/tasashi0805/ICT-turtlebot


Install ROS:
	
	check the current Ubuntu version.
	Recommand using the ubuntu 20 LTS and ROS Noetic to launch this project.
	Recommand install ubuntu in the operating system. Don't use the virtual machine.
	The following link is an instruction to install ROS
	https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup
	The link is an ubuntu 20LTS download
	https://releases.ubuntu.com/20.04/

Network:

	if you are using the UNISA network to test the program you might switch your IP:
	
	1 $ nano ~/.bashrc 
	in the last line two line  switch the ip as
	2 export ROS_MASTER_URI=http://localhost:11311
	3 export ROS_HOSTNAME=localhost
	optional command for export the turtlebot waffle it will automatically export the turtlebot before you launch the world so you don't have type it before launch the map
	4 export TURTLEBOT3_MODEL=waffle	
	5 save and exit the test editor
	
	$ source ~/.bashrc 

Set up enviorment

	1. Install python Open CV
		$ sudo apt update
		$ sudo apt install python3-pip
		$ pip install opencv-python
	2. The ICT-turtlebot-Project folder need to be move into ~/home/catkin_ws/src

	3. My_ground_plane  folder need to be move into ~/home/.gazebo/models

	4. In terminal $ ~/home/catkin_ws/src/ICT-turtlebot-Project chmod +x *.py

	5. you might need a dos2unix on obstacle python file
		$ sudo apt-get install dos2unix
		$ dos2unix pythonfile.py
 
#Starting the simulator

In terminal:
	
	
	(if you followed the Network part you don't have to follow the 1 step)	
	1. export TURTLEBOT3_MODEL=waffle 
	launch the simulator world
	2. roslaunch project projectworld.launch
	In new termainl (ctrl + t)
	launch the python file
	3. roslaunch project Combine.launch

# Reopen the simulator

	In terminal
		$ killall gzcleint
		$ killall gzsever
		
		
# file for implement to real world
	1.colordetectBot.py
	2.obstacleavoidance_map.py
	3. Drive.py

