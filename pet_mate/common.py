class ClarificationNeeded(Exception):
    def __init__(self, question):
        self.question = question
        super().__init__(question)