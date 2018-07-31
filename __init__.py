# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
import nltk
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import nltk
from nltk.stem.porter import *

__author__ = 'asalekin'

LOGGER = getLogger(__name__)


class RobotGoSkill(MycroftSkill):
    def __init__(self):
        super(RobotGoSkill, self).__init__(name="RobotGoSkill")
        stemmer = PorterStemmer()

    def initialize(self):
        robot_go_intent = IntentBuilder("RobotGoIntent").require("RobotGoKeyword").build()
        self.register_intent(robot_go_intent, self.handle_robot_go_intent)

        robot_stop_intent = IntentBuilder("RobotStopIntent").require("RobotStopKeyword").build()
        self.register_intent(robot_stop_intent, self.handle_robot_stop_intent)

    def handle_robot_go_intent(self, message):
        #Dest_word = message.data.get("Word")
        #if message.data.get("robot"):
        #    Robot_name= message.data.get("robot")
        #else"
        #    Robot_name= 'None'

        allwords=message.data.get('utterance')

        output=stemmer.stem(allwords)


        self.speak(output, expect_response=True)



    def handle_robot_stop_intent(self, message):

        allwords=message.data.get('utterance')

        self.speak_dialog('stop')
          


    def stop(self):
        pass


def create_skill():
    return RobotGoSkill()
