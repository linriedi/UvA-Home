
from interaction.hearing import Hearing
from interaction.speech import Speech
from opendag_IR import OpendagIR
from language_processing import LanguageProcessing
from naoqi import Naoqi
import datetime
from random import randint

class RosterPresenter:
    def __init__(self, naoqi):
        self.naoqi = naoqi
        self.hearing = Hearing(self.naoqi)
        self.speech = Speech(self.naoqi)
        self.ir = OpendagIR()
        self.nlp = LanguageProcessing()

    def present(self):
        self.speech.say("Hi!")

        while True:
            sentence = self.hearing.recognize().lower()
            print("Sentence: " + sentence)
            command = self.nlp.get_command(sentence)
            if command:
                if command[0] == "greeting":
                    self.speech.say("Greetings human!")
<<<<<<< HEAD
                    q = ["Greetings human!", "Hi there!", "Hi!"]
                    answer = q[randint(0,len(q)-1)]
=======

                elif command[0] == "break":
                    self.speech.say("I won't be listening for a vew seconds")
                elif command[0] == "robot_name":
                    self.speech.say("My name is Mickey")
>>>>>>> 1ebe12e52dc33ec7a19be872cb764dce04e32d54
                elif command[0] == "goodbye":
                    q = ["Goodbye and enjoy your day!", "See you later!", "Goodbye!", "Later, sucker!", "Please don't leave me here with all these people!", "Cheers mate!", "Please don't go!"]
                    answer = q[randint(0,len(q)-1)]
                    self.speech.say(answer)
<<<<<<< HEAD
                break
=======
            break
>>>>>>> 1ebe12e52dc33ec7a19be872cb764dce04e32d54
        print("Done")
