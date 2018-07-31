from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler



class PptControllerSkill(MycroftSkill):
    def __init__(self):
        super(PptControllerSkill, self).__init__(name="PptControllerSkill")
        self.file_opened = False

    @intent_handler(IntentBuilder("PPTIntent").require('PptController'))
    def handle_ppt_controller(self, message):
        self.speak_dialog('ppt.controller')

    @intent_handler(IntentBuilder("OpenPPTIntent").require('OpenPPT').require("Filename"))
    def handle_ppt_open(self, message):
        filename = message.data.get("Filename")
        self.file_opened = True
        # Send a rest request
        param = {'filename':filename}
        resp = {'filename' : filename}
        self.speak_dialog('ppt.open', data=resp)

    @intent_handler(IntentBuilder("NextSlideIntent").require('NextSlide'))
    def handle_next_slide(self, message):
        if self.file_opened:
            self.speak_dialog('ppt.next')
        else:
            self.speak_dialog('ppt.filenotopen')

    @intent_handler(IntentBuilder("PrevSlideIntent").require('PrevSlide'))
    def handle_prev_slide(self, message):
        if self.file_opened:
            self.speak_dialog('ppt.prev')
        else:
            self.speak_dialog('ppt.filenotopen')

    @intent_handler(IntentBuilder("ClosePPTIntent").require('ClosePPT'))
    def handle_ppt_close(self, message):
        if self.file_opened:
            self.speak_dialog('ppt.close')
        else:
            self.speak_dialog('ppt.filenotopen')

    def create_skill():
        return PptControllerSkill()

