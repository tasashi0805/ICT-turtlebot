# ICT-Turtlebot-Project
Install ROS:
	check the current Ubuntu version.
	Recommand using the ubuntu 20 LTS and Noetic to launch this project.
	Recommand install ubuntu in the operating system. Don't use the virtual machine.
	https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup

Network:

	if you are using the UNISA network to test the program you might switch your IP:
	
	1 $ nano ~/.bashrc 
	to the last line two line  switch the ip as
	2 export ROS_MASTER_URI=http://localhost:11311
	3 export ROS_HOSTNAME=localhost
	optional command for export the turtlebot waffle it will automatically export the turtlebot before you launch the world
	4 export TURTLEBOT3_MODEL=waffle	
	5 save and exit the test editor
	
	$ source ~/.bashrc 

Set up enviorment

	1. Install python Open CV
		$ sudo apt update
		$ sudo apt install python3-pip
		$ pip install opencv-python
	2. The folder need to be move into ~/home/catkin_ws/src

	3. My_ground_plane  folder need to be move into ~/home/.gazebo/models

	In terminal
	4. $ chmod +x python file

	5. you might need a dos2unix on obstacle python file

		$ sudo apt-get install dos2unix
		$ dos2unix pythonfile.py
 
#Starting the simulator

In terminal:
	
	(if you followed the Network part you don't have to follow the 1 step)	
	1. export TURTLEBOT3_MODEL=waffle 


	launch the simulator world
	2. roslaunch project projectworld.launch

	launch the python file
	3. roslaunch project Combine.launch

# Reopen the simulator

	In terminal
		$ killall gzcleint
		$ killall gzsever
# Git hub link
	https://github.com/tasashi0805/ICT-turtlebot/tree/main
