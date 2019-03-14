
class JudgementEntity:

    def __init__(self, id, text, acquittal=False, conditional=False, rejected=False, verdict=False, warning=False):
        self._id = id
        self._text = text
        self._acquittal = acquittal
        self._conditional = conditional
        self._rejected = rejected
        self._verdict = verdict
        self._warning = warning
    
    