from mycroft.skills.core import FallbackSkill


class MeaningFallback(FallbackSkill):
    """
        A Fallback skill to answer the question about the
        meaning of life, the universe and everything.
    """
    def __init__(self):
        super(MeaningFallback, self).__init__(name='Meaning Fallback')

    def initialize(self):
        """
            Registers the fallback skill
        """
        self.register_fallback(self.handle_fallback, 1)
        # Any other initialize code goes here

    def handle_fallback(self, message):
        """
            Answers question about the meaning of life, the universe
            and everything.
        """
        utterance = message.data.get("utterance")

        # get keywords for current language
        what = self.dialog_renderer.render('query')
        meaning = self.dialog_renderer.render('meaning')
        life = self.dialog_renderer.render('life')
        universe = self.dialog_renderer.render('universe')
        everything = self.dialog_renderer.render('everything')

        if what in utterance \
            and meaning in utterance \
            and (life in utterance \
                or universe in utterance \
                or everything in utterance):
            self.speak('42', expect_response=True)
            return True # Indicate that the utterance was handled
        else:
            return False

    def shutdown(self):
        """
            Remove this skill from list of fallback skills.
        """
        self.remove_fallback(self.handle_fallback)
        super(MeaningFallback, self).shutdown()


def create_skill():
    return MeaningFallback()
