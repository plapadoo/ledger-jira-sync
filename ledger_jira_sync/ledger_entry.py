class LedgerEntry(object):
    def __init__(self, time_spent_seconds, author, date, account, comment=None):
        self.time_spent_seconds = time_spent_seconds
        self.author = author
        self.date = date
        self.account = account
        self.comment = comment

    def __repr__(self):
        return "{"+str(self.time_spent_seconds)+", "+self.author+", "+str(self.date)+", "+str(self.account)+", "+str(self.comment)+"}"

    def __hash__(self):
        return hash((self.time_spent_seconds, self.date, self.account))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.time_spent_seconds == other.time_spent_seconds and self.date == other.date and self.account == other.account
        return False
