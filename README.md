# Intruder-Detector
This project uses a Raspberry Pi and mobile device to sound an alarm when a person is visible. 

## Requirements
Hardware needed for this project include:
- A full Raspberry Pi desktop setup with monitor, keyboard, mouse, etc.
- A breadboard 
- 3 LEDs (green, yellow, and red)
- 3 330 Ω resistors
- A push-to-make switch
- A small loudspeaker
- ≥5 male to female jumper connectors (5 for components and 2 for power)
- male to male jumper connectors/solid-core 22 AWG wire (for buzzer and button)
- An Android/iOS device

All software for the Raspberry Pi is available here however to remotely access a mobile device's camera we will use a free open-source software called DroidCam by Dev47Apps. 
The download links for this are shown below:

Android: https://play.google.com/store/apps/details?id=com.dev47apps.droidcam

iOS: https://apps.apple.com/us/app/droidcam-webcam-obs-camera/id1510258102

## Setup

Connect the Raspberry Pi GPIO (General Purpose Input and Output) to the components as shown in the circuit schematic below:

![wiring_diagram](https://user-images.githubusercontent.com/66517600/128150007-c6867979-26f9-4659-bc37-539a601ae165.png)

Here is an example wiring diagram using a Raspberry Pi 2 and a half-sized breadboard:

![breadboard_layout](https://user-images.githubusercontent.com/66517600/128152397-84f5ca5a-f20d-4ebb-9bc0-c07c89f33d10.png)

Color code:
- Red - +5V 
- Black - GND (0V)
- Green - Input 
- Blue - Output

If you wish to use any other GPIO pins other than the ones used in the wiring diagram, you will need to modify the settings.ini file. There, you will also find other configuration data which you can modify such as the IP address and port of the device running DroidCam.

Install Raspberry Pi OS on an SD card and go through all the installation steps. 
Next, download and run the installation script as shown below. This should take a few minutes. 

```
$ git clone https://github.com/The-H4CKER/intruder-detector.git
$ cd intruder-detector/
$ chmod +x detector.sh 
$ ./detector.sh -i # Installs all dependencies for first-time usage
```

## Usage

Open DroidCam on your device. To start detection from the Raspberry Pi, simply run:
```
$ ./detector.sh
```
There will be a delay in the video output due to the processing time of the Pi. The size of this will depend on exactly which board you have.

## Example Output

![example_output](https://user-images.githubusercontent.com/66517600/128157693-19d460a1-39a8-4919-b468-a4325cf219f2.png)
