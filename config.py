import cv2 as cv
import requests
import RPi.GPIO as GPIO
from configparser import ConfigParser
from gpiozero import LED, Button
from re import match
from time import sleep


RED = (0, 0, 0xFF)
GREEN = (0, 0xFF, 0)
firstRun = True

connections = []
config = ConfigParser()
config.read("settings.ini")


class Buzzer:
    def __init__(self, pin, speed, repeat):
        self.pin = pin
        self.speed = speed
        self.repeat = repeat

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(self.pin), GPIO.OUT)

    def beep(self):
        p = GPIO.PWM(26, 50)
        p.start(70)
        for i in range(self.repeat):
            for x in range(200, 2200):
                p.ChangeFrequency(x)
                sleep(self.speed)
        p.stop()


def raiseException(error, info):
    if error == "CONNECTION_FAILURE":
        print(
            "Failed to connect. Please check that DroidCam is active and the correct IP address is being used."
        )
    elif error == "CORRUPTED_FILE":
        print("Settings.ini file is corrupted.")
    else:
        print("Invalid entry in settings.ini file under %s" % error)
    print("See error log below:\n")
    raise Exception(info)


try:
    # Verifying server in settings.ini file
    if match(
        r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$",
        # Regex for IPv4 address
        config["DROIDCAM_SERVER"]["IP"],
    ):
        IP = config["DROIDCAM_SERVER"]["IP"]
    else:
        raiseException("DROIDCAM_SERVER - IP", "Invalid IP address format.")

    try:
        if 0 <= int(config["DROIDCAM_SERVER"]["Port"]) <= 65535:
            PORT = int(config["DROIDCAM_SERVER"]["Port"])
        else:
            raiseException(
                "DROIDCAM_SERVER - Port", "Port numbers must be between 0 and 65535"
            )
    except ValueError as e:
        raiseException("DROIDCAM_SERVER - Port", str(e))

    # Verifying GPIO connections in settings.ini file
    try:
        for i in config["GPIO_CONNECTIONS"].values():
            connections.append(int(i))
    except ValueError as e:
        raiseException("GPIO_CONNECTIONS", e)

    connections.sort()
    uniqueConnections = list(set(connections))
    uniqueConnections.sort()

    if connections == uniqueConnections and connections[0] > 1 and connections[-1] < 28:
        redLED = LED(int(config["GPIO_CONNECTIONS"]["RedLED"]))
        yellowLED = LED(int(config["GPIO_CONNECTIONS"]["YellowLED"]))
        greenLED = LED(int(config["GPIO_CONNECTIONS"]["GreenLED"]))
        button = Button(int(config["GPIO_CONNECTIONS"]["Button"]))
        buzzer = Buzzer(int(config["GPIO_CONNECTIONS"]["Buzzer"]), 0.001, 3)
        buzzer.initialize()
    else:
        raiseException(
            "GPIO_CONNECTIONS",
            "GPIO pins must be between 2 and 27 and cannot be repeated",
        )
except Exception as e:
    raiseException("CORRUPTED_FILE", e)


def alert():
    greenLED.blink(0.1)
    yellowLED.blink(0.1)
    redLED.blink(0.1)
    buzzer.beep()
    sleep(10)


# Verifying image recognition values from settings.ini file
try:
    if 0 <= float(config["IMAGE_RECOGNITION"]["ProbabilityCorrect"]) <= 1:
        ACCURACY = float(config["IMAGE_RECOGNITION"]["ProbabilityCorrect"])
    else:
        raiseException(
            "IMAGE_RECOGNITION - ProbabilityCorrect",
            "Probability is not between 0 and 1",
        )
except ValueError as e:
    raiseException("IMAGE_RECOGNITION - ProbabilityCorrect", e)


# Required config and weight paths to provide analysis
classFile = "coco.names"
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"
classNames = []

with open(classFile, "r") as f:
    classNames = f.read().rstrip("\n").split("\n")

# Configuring image recognition model
net = cv.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Testing connection to DroidCam server
try:
    r = requests.head("http://%s:%d/video" % (IP, PORT), stream=True)
except Exception as e:
    raiseException("CONNECTION FAILURE", e)

cap = cv.VideoCapture("http://%s:%d/video" % (IP, PORT))
