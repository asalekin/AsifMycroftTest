from mycroft.skills.core import FallbackSkill


class MeaningFallback(FallbackSkill):
    """
        A Fallback skill to answer the question about the
        meaning of life, the universe and everything.
    """
    match_words=['robot', 'drone', 'machine']
    store={}
    talkstring=0
    
    def __init__(self):
        super(MeaningFallback, self).__init__(name='Meaning Fallback')

    def initialize(self):
        """
            Registers the fallback skill
        """
        self.register_fallback(self.handle_fallback, 1)
        #self.store={}
        self.store[0]='1'
        self.store[1]='5'
        self.store[2]='7'
        self.store[3]='10'
        #self.talkstring=0
        # Any other initialize code goes here

    def handle_fallback(self, message):
        """
            Answers question about the meaning of life, the universe
            and everything.
        """
        utterance = message.data.get("utterance")

        # get keywords for current language
        robot = self.dialog_renderer.render('robot')

        if any(i in utterance for i in self.match_words):               #robot in utterance:


            self.speak("Asif said "+self.store[self.talkstring]+" "+utterance, expect_response=True)
        
            self.talkstring=self.talkstring+1
            if self.talkstring>3:
                self.talkstring=0
            return True # Indicate that the utterance was handled
        else:
            self.speak("Skill end and asif said "+utterance)
            return False

    def shutdown(self):
        """
            Remove this skill from list of fallback skills.
        """
        self.remove_fallback(self.handle_fallback)
        super(MeaningFallback, self).shutdown()


def create_skill():
    return MeaningFallback()
