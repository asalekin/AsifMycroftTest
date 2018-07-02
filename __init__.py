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

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'asalekin'

LOGGER = getLogger(__name__)


class RobotGoSkill(MycroftSkill):
    def __init__(self):
        super(RobotGoSkill, self).__init__(name="RobotGoSkill")

    def initialize(self):
        robot_go_intent = IntentBuilder("RobotGoIntent").require("RobotGoKeyword").require("Word").build()
        self.register_intent(robot_go_intent, self.handle_robot_go_intent)

        robot_back_intent = IntentBuilder("RobotBackIntent").require("RobotBackKeyword").require("Word").build()
        self.register_intent(robot_back_intent, self.handle_robot_back_intent)


    def handle_robot_go_intent(self, message):
        toplaceword = message.data.get("Word")
        
        self.speak_dialog("move")
        self.speak(toplaceword)

        print(message)

    def handle_robot_back_intent(self, message):
        fromplaceword = message.data.get("Word")
        
        self.speak_dialog("back")
        self.speak(fromplaceword)



    def stop(self):
        pass


def create_skill():
    return RobotGoSkill()
