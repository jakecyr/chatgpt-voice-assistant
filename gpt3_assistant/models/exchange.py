class Exchange:

    def __init__(self, user, computer, was_cut_short=None):
        self._user = user
        self._computer = computer
        self._was_cut_short = was_cut_short

    def was_cut_short(self):
        return self._was_cut_short

    def set_was_cut_short(self, was_cut_short):
        self._was_cut_short = was_cut_short

    def get_user_message(self):
        return self._user

    def get_computer_response(self):
        return self._computer
