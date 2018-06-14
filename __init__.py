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


class RobotMoveSkill(MycroftSkill):
    def __init__(self):
        super(RobotMoveSkill, self).__init__(name="RobotMoveSkill")
        self.file_opened = False


    @intent_handler(IntentBuilder("RobotGoIntent").require('RobotGoKeyword').require("Position"))
    def handle_robot_go(self, message):

	place_name = message.data.get("Position")
        self.emitter.once("recognizer_loop:audio_output_start", self.enclosure.mouth_text(place_name))
        
        self.enclosure.deactivate_mouth_events()
	self.speak(place_name)

        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()


    def stop(self):
        pass


def create_skill():
    return RobotMoveSkill()
