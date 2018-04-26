def seconds_to_human(s):
    return str(s / 3600) + 'h ' + str(s % 3600 / 60) + "m"

class Entry(object):
    def __init__(self, time_spent_seconds, author, date, account, jira_id, jira_log, comment):
        self.time_spent_seconds = time_spent_seconds
        self.author = author
        self.date = date
        self.account = account
        self.jira_id = jira_id
        self.jira_log = jira_log
        self.comment = comment

    def __repr__(self):
        return self.jira_id+": "+self.date+" "+seconds_to_human(self.time_spent_seconds)

    def __hash__(self):
        return hash((self.time_spent_seconds, self.date, self.account, self.jira_id))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.time_spent_seconds == other.time_spent_seconds and self.date == other.date and self.jira_id == other.jira_id
        return False
