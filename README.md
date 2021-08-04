# Intruder-Detector
This project uses a Raspberry Pi and mobile device to sound an alarm when a person is visible. 

## Requirements
Hardware needed for this project include:
- A full Raspberry Pi desktop setup with monitor, keyboard, mouse etc.
- A breadboard 
- 3 LEDs (green, yellow and red)
- 3 330Ω resistors
- A push to make switch
- A small loudspeaker
- >=5 male to female jumper connectors (5 for components and 2 for power)
- male to male jumper connectors/solid-core 22 AWG wire (for buzzer and button)
- An Android/iOS device

All software for the Raspberry Pi is avaliable here however to remotely access a mobile device's camera we will use a free open-source software called DroidCam by Dev47Apps. 
The download links for this are shown below:

Android: https://play.google.com/store/apps/details?id=com.dev47apps.droidcam

iOS: https://apps.apple.com/us/app/droidcam-webcam-obs-camera/id1510258102

## Setup

Connect the Raspberry Pi to the components as shown in the diagrams below:

![breadboard_layout](https://user-images.githubusercontent.com/66517600/128146519-ac6165b2-75e6-4515-b3d9-959086e1d5ea.png)

Here is the circuit schematic:

![wiring_diagram](https://user-images.githubusercontent.com/66517600/128146259-6c0dbd62-e9f7-4ff8-a83e-eef444c73855.png)


## Usage

Install Raspberry Pi OS on a SD card and go through all the installation steps.

Installation is as follows:
```
pi@raspberrypi:~ $ git clone https://github.com/The-H4CKER/Intruder-Detector.git
pi@raspberrypi:~ $ cd Intruder-Detector/
pi@raspberrypi:~/Intruder-Detector $ chmod +x main.sh 
pi@raspberrypi:~/Intruder-Detector $ ./main.sh -i # Installs all dependencies for first-time usage
```
To start detection, simply run:
```
pi@raspberrypi:~/Intruder-Detector $ ./main.sh
```


