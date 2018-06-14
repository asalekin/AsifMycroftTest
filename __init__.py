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
        robot_go_intent = IntentBuilder("RobotGoIntent").require("RobotGoKeyword").require("Word1").optionally("Word0").build()
        self.register_intent(robot_go_intent, self.handle_robot_go_intent)



    def handle_robot_go_intent(self, message):
        toplaceword = message.data.get("Word1")
        
        fromplaceword = message.data.get("Word0")
        From_location = self.get_spoken_time(fromplaceword)

        self.speak_dialog("welcome")
        self.speak(toplaceword)
        if not current_time:
            self.speak(fromplaceword)




    def stop(self):
        pass


def create_skill():
    return RobotGoSkill()
