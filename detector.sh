#!/bin/bash

function startDetection(){
	printf "Starting main.py...\n"
	source env/bin/activate
	python main.py
}

function notInitialized(){
	printf "\nAn unexpected error has occurred. "
	printf "Have you initialized the program?\n"
	printf "Try running '%s -i' first.\n" "${0}"
}

function usage(){
	printf "Usage: %s [OPTIONS]\n" "${0}"
	printf " -h, --help Shows help\n"
	printf " -i, --init Initializes the program.\n"
	printf " -r, --run  Starts the detector.\n"
	printf "If no arguments are supplied, " 
	printf "the script will default to starting the detector.\n"
}

if [ -z "$1" ]
	then
		startDetection || notInitialized
else
	case $1 in
	-h|--help)
		usage
		;;
	-i|--init)
		printf "Updating system...\n\n"
		sudo apt update
		sudo apt upgrade -y

		printf "\nSetting up virtual environment...\n\n"
		python3 -m venv env
		source env/bin/activate

		printf "Installing OpenCV...\n\n"
		sudo apt install python-opencv -y
		sudo apt install libatlas3-base 

		printf "\nUpdating pip for %s...\n\n" "$(python -V)"
		# opencv-python require pip3 >= 19.3
		pip install pip --upgrade pip

		printf "\nInstalling required libraries...\n\n"
		pip install gpiozero requests RPi.GPIO opencv-python

		printf "\nDone.\n\n"

		while true
		do
			read -r -p "Would you like to start detection now? [Y/n] " runScript
		
			case ${runScript,,} in
			[yY][eE][sS]|[yY])
			startDetection
			break
			;;
			[nN][oO]|[nN])
			printf "Terminating program.\n"
			break
			;;
			*)
			printf "Invalid input... "
			;;
			esac
		done
		;;
	-r|--run)
		startDetection || notInitialized
		;;
	*)
		printf "Invalid command. Run '%s -h' for usage.\n" "${0}"
		;;
	esac
fi
