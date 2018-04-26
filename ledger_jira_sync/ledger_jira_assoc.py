class LedgerJiraAssoc(object):
    def __init__(self, jira_ticket, with_comment):
        self.jira_ticket = jira_ticket
        self.with_comment = with_comment

def read_ledger_jira_assoc(filename):
    result = {}
    with open(filename) as f:
        for line in f.readlines():
            if line == '':
                continue
            split = line.strip().split("=")
            if len(split) != 2:
                raise Exception('line not of the form \"foo=bar\"')
            with_comment = False
            jira_ticket = split[1]
            if split[1][0:2] == 'c:':
                with_comment = True
                jira_ticket = split[1][2:]
            result[split[0]] = LedgerJiraAssoc(jira_ticket, with_comment)
    return result
