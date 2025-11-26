class ClarificationNeeded(Exception):
    def __init__(self, question):
        self.question = question
        super().__init__(question)


class GuessConfirmationNeeded(Exception):
    def __init__(self, question, guess_details):
        self.question = question
        self.guess_details = guess_details  # Contains the guess information (pet name, image URL, etc.)
        super().__init__(question)