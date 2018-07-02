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
from adapt.engine import IntentDeterminationEngine
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'asalekin'

LOGGER = getLogger(__name__)


class RobotGoSkill(MycroftSkill):
    def __init__(self):
        super(RobotGoSkill, self).__init__(name="RobotGoSkill")

    def initialize(self):

        robot_keyword=["robot", "drone"]
        for rk in robot_keyword:
            self.register_entity(rk, "RobotKeyword")

        robot_move=["go", "move", "monitor", "view", "surveil"]
        for rm in robot_move:
            self.register_entity(rm, "RobotMove")

        robot_location=["place one", "place two", "place three", "area one", "area two", "area three", "point one", "point two", "point three", "spot one", "spot two", "spot three", "zone one", "zone two", "zone three"]
        for rl in robot_location:
            self.register_entity(rl, "RobotLocation")


        robot_go_intent = IntentBuilder("RobotGoIntent").require("RobotKeyword").optionally("RobotMove").require("RobotLocation").build()
        self.register_intent(robot_go_intent, self.handle_robot_go_intent)



    def handle_robot_go_intent(self, message):
        #toplaceword = message.data.get("Word")
        
        self.speak_dialog("move")
        #self.speak(toplaceword)


    def stop(self):
        pass


def create_skill():
    return RobotGoSkill()
