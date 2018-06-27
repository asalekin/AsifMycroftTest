import requests
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import getLogger


class RobotGoSkill(MycroftSkill):
    def __init__(self):
        super(RobotGoSkill, self).__init__(name="RobotGoSkill")

    @intent_handler(IntentBuilder("RobotIntent").require('send'))
    def handle_robot_controller(self, message):
        print(message)

    @intent_handler(IntentBuilder("OpenPPTIntent").require('OpenPPT').require("Filename"))
    def handle_ppt_open(self, message):
        filename = message.data.get("Filename")
        print(filename)


def create_skill():
    return RobotGoSkill()

