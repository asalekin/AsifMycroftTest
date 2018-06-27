import requests
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger


class PptControllerUsingPadatiousSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.file_opened = False

    @intent_file_handler('ppt.controller.intent')
    def handle_ppt_controller_using_padatious(self, message):
        self.speak_dialog('ppt.controller.using.padatious')

    @intent_file_handler('ppt.open.intent')
    def handle_ppt_open(self, message):
        filename = message.data.get("filename")
        if filename is None:
            self.speak_dialog('ppt.specifyfile')
        else:	
            self.file_opened = True;
            resp = {'filename' : filename}
            self.speak_dialog('ppt.open', data=resp)


    @intent_file_handler('ppt.next.intent')
    def handle_next_slide(self, message):
    if self.file_opened: 
        self.speak_dialog('ppt.next')


    @intent_file_handler('ppt.prev.intent')
    def handle_prev_slide(self, message):
        self.speak_dialog('ppt.prev')


    @intent_file_handler('ppt.close.intent')
    def handle_ppt_close(self, message):
        self.speak_dialog('ppt.close')

def create_skill():
    return PptControllerUsingPadatiousSkill()

