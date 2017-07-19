# MAIN File
# Sculpted with love by Thomas Groot en Jonathan Gerbscheid <3

# Naoqi Imports #
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# additional Imports
import math
import time
import sys
import Image
import numpy
import cv2
# Local modules #
import facedetection
import facerecognition
import speech
import slam
from Sound import locateSound # jonathans naoqi stuff
from PeopleDetection import peopledetector

# Global variables #
# IP = "127.0.0.1"
IP = "pepper.local"
# IP = "146.50.60.15"
PORT = 9559

TextToSpeech = None
VideoDevice = None
AudioRecorder = None
AudioDevice = None
SoundLocator = None
Navigation = None
Localizer = None
memory = None
motionProxy  = None
postureProxy = None
pplDetectionargs = None


#############
# Functions #
#############


# jonathan comment dit
def setup_people_detection():
    global pplDetectionargs
    pplDetectionargs = peopledetector.setup_network()

# jonathan comment dit
def detect_people():
    return peopledetector.detect_people(VideoDevice, *pplDetectionargs)

# return detected faces
def make_face_database(tracking=False):
    global VideoDevice
    if tracking:
        if motionProxy == None:
            init_localization()
        print("Finding faces...")
        face_list = facedetection.collect_faces(VideoDevice, motionProxy)
    else:
        print("Finding faces...")
        face_list = facedetection.collect_faces(VideoDevice)
    return face_list

# Detects faces in one image
def detect_faces():
    global VideoDevice
    face_list = facedetection.detect_once(VideoDevice)
    return face_list

# Train a set of faces to be associated with a label
def train_recognize_faces(face_list, labels, recognizer=None):
    if recognizer == None:
        recognizer = facerecognition.FaceRecognizer()
    print("Training faces...")
    recognizer.train(face_list, labels)
    return recognizer

# Return names from a list of recognized faces
def recognize_faces(recognizer):
    global VideoDevice
    print("Recognizing faces...")
    recognized_faces = recognizer.recognize(VideoDevice)
    return recognized_faces

# Testing speech synthesis
def speech_test(text="Hi human"):
    global TextToSpeech
    TextToSpeech.say(text)

# Return recognized speech
def speech_recognition(max_tries = 4):
    global AudioRecorder
    global AudioDevice
    print("Recognizing speech...")
    tries = 0
    sentence = ""
    while tries < max_tries and sentence == "":
        sentence = speech.wait_for_voice(AudioRecorder, AudioDevice)
        tries += 1
    return sentence


######################
# Proxy Initializers #
######################


# Allows the robot to say text
def init_textToSpeech():
    global TextToSpeech
    TextToSpeech = ALProxy("ALTextToSpeech", IP, 9559)

# Soundlocator is for locating sound
def init_soundLocalization():
    global SoundLocator
    SoundLocator = locateSound.SoundLocatorModule("SoundLocator")

# Videodevice is for taking images from the videostream
def init_videoDevice():
    global VideoDevice
    VideoDevice = ALProxy("ALVideoDevice", IP, 9559)

# AudioRecorder is for sound recording
def init_audioRecorder():
    global AudioRecorder
    AudioRecorder = ALProxy("ALAudioRecorder", IP, 9559)

# AudioDevice is for sound level registration
def init_audioDevice():
    global AudioDevice
    AudioDevice = ALProxy("ALAudioDevice", IP, 9559)

# Navigation module
def init_navigation():
    global Navigation
    Navigation = ALProxy("ALNavigation", IP, 9559)

def init_motion():
    global motionProxy
    global postureProxy
    motionProxy = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)
    motionProxy.wakeUp()

def init_localization():
    global Localizer
    Localizer = slam.Localization(Navigation)


########
# Main #
########

def turn_to_sound():
    if SoundLocator.soundFound:
        # move to the source of the sound
        print("angle found: " + str(SoundLocator.soundAngle))
        motionProxy.moveTo(0.0, 0.0, math.radians(SoundLocator.soundAngle))
        SoundLocator.reset_variables()


def get_biggest_box_index(boxlist):
    index = None
    maxsize = 0
    for i in range(len(boxlist)):
        width = boxlist[i][2] - boxlist[i][0]
        height = boxlist[i][3] - boxlist[i][1]
        size = width * height
        if size > maxsize:
            maxsize = size
            index = i
    return index


def cocktail_party():
    # this function gives an outline of how the cocktail_party function should look

	# STEP 1: ENTER ROOM
		# localize to center of room -> done-ish
    Localizer.move_to([0,0])

	# STEP 2: getting called
	# find a person and approach them
    setup_people_detection()
    init_soundLocalization()
    while True:
        turn_to_sound()
        peopleList = detect_people()
        if len(peopleList) > 0:
            continuousdetection = True
            for _ in range(4):
                peopleList = detect_people()
                if len(peopleList) == 0:
                    continuousdetection = False
            if continuousdetection:
                break
    speech_test("I found you!")
    boxindex = get_biggest_box_index(peopleList)
    # turn to person
    # move to person


        # person can be calling, waving, or with an arm raised
        # EITHER:
            # sound localize correct person --> done
            # detect random person in room --> done

        # move towards person, -> need distance measure

        # learn person     -> face recognition done
        #                -> guide person in face recognition

    # STEP 3: taking the order
    # place the order

        # tak additional orders from customers
        # FKIN NOPE
    # STEP 4: sitting person

        # do the same stuff as 2 but for a sitting person that does not call
        # for help
        # sitting people detector: --> filter on shape of detections
        # NOPE

    # STEP 5: placing orders
        # repeat drink, name and person description

    # STEP 6,7,8: we are skipping these
    print("nothing here")


def general_purpose_service():
    print("nothing here")

# Main function that is run once upon startup
def main():
    lifeProxy = ALProxy("ALAutonomousLife", IP, PORT)
    # lifeProxy.setState("disabled")
    print("AutonomousLife: " + lifeProxy.getState())
    # init_soundLocalization()
    init_navigation()
    init_textToSpeech()
    init_videoDevice()
    init_motion()
    init_audioDevice()
    init_audioRecorder()
    init_localization()
    # setup_people_detection()
    # Localizer.explore(2)
    # Localizer.stop_exploration()

    # test_main.main()
    # setup_people_detection()
    # look around for a crowd

    # # find ppl
    # motionProxy.stopMove()
    # time.sleep(5)

    # correct head position
    # currentAngle = motionProxy.getAngles("HeadYaw", True)[0]
    # motionProxy.setAngles("HeadPitch", currentAngle + 0.08, 0.2)
    speech_test()
    # Localizer.explore(15)
    # Localizer.save_exploration()
    Localizer.stop_localization()
    Localizer.load_exploration("/home/nao/.local/share/Explorer/2017-07-19T163238.071Z.explo")
    # print("path: " + str(Localizer.map_path))
    # result_map = Localizer.map
    # map_width = result_map[1]
    # map_height = result_map[2]
    # img = numpy.array(result_map[4]).reshape(map_width, map_height)
    # img = (100 - img) * 2.55 # from 0..100 to 255..0
    # img = numpy.array(img, numpy.uint8)
    # cv2.imwrite("iismap.png", img)
    # Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()
    # print("start talking")
    # sentence = speech_recognition()
    # print(sentence)
    Localizer.start_localization()
    Localizer.relocalize([0.,0.])
    # Localizer.move_to([-1., -1.])
    print("estimate location: " + str(Localizer.get_robot_position()))
    # Localizer.stop_exploration()

    # MAIN WHILE LOOP
    # while True:
    #     # do a lot of stuff here
    #     peopleList = detect_people()
    #     print("found " + str(len(peopleList)) + " people!")
    #
    #     # finally turn to sound if it was recognized
    #     if SoundLocator.soundFound:
    #         # move to the source of the sound
    #         print("angle found: " + str(SoundLocator.soundAngle))
    #         motionProxy.moveTo(0.0, 0.0, math.radians(SoundLocator.soundAngle))
    #         SoundLocator.reset_variables()

    print("Done")


# Use the main function
if __name__ == "__main__":
    main()
