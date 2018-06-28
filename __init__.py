# Copyright 2017, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import dirname, join

import pyjokes

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from random import choice


joke_types = ['chuck', 'neutral']


class JokingSkill(MycroftSkill):
    def __init__(self):
        super(JokingSkill, self).__init__(name="JokingSkill")

    def speak_joke(self, lang, category):
        self.speak(pyjokes.get_joke(language=lang, category=category))

    @intent_file_handler('go.robot.intent')
    def handle_ppt_open(self, message):
        filename = message.data.get('filename')
        self.speak_dialog(filename)

    def stop(self):
        pass


def create_skill():
    return JokingSkill()
