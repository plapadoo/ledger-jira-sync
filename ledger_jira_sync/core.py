from datetime import datetime, tzinfo, timedelta
from jira import JIRA
from ledger_jira_sync.entry import Entry
from ledger_jira_sync.ledger_jira_assoc import read_ledger_jira_assoc
from ledger_jira_sync.ledger_parser import read_ledger

class UTC(tzinfo):
    def utcoffset(self, _):
        return timedelta(0)
    def tzname(self, _):
        return "UTC"
    def dst(self, _):
        return timedelta(0)

def entry_from_ledger_entry(e, ticket_mappings):
    if str(e.account) not in ticket_mappings:
        return None
    mapping = ticket_mappings[str(e.account)]
    return Entry(int(e.time_spent_seconds) // 60 * 60, e.author, str(e.date), e.account, mapping.jira_ticket, None, e.comment if mapping.with_comment else '')

def jira_logs(jira_client, email, ledgertag, account, ticket_id):
    print 'Getting logs for '+ticket_id
    logs = [log for log in jira_client.worklogs(ticket_id) if log.author.emailAddress == email]
    result = []
    for log in logs:
        # conversion to str for date: it's u'2018-04-30' otherwise
        log.jiraIssueId = ticket_id
        result.append(Entry(log.timeSpentSeconds, ledgertag, str(log.started[0:10]), account, ticket_id, log, None))
    return result

def determine_adds_and_deletes(jira_client, email, ledgertag, ticket_mappings, all_ledger_entries):
    entries = []
    for le in all_ledger_entries:
        e = entry_from_ledger_entry(le, ticket_mappings)
        if e:
            entries.append(e)

    grouped_entries = {e.jira_id : [entry for entry in entries if entry.jira_id == e.jira_id] for e in entries}

    entries_to_add = []
    entries_to_remove = []
    for jira_id, ledger_entries in grouped_entries.iteritems():
        entries_to_add.extend(ledger_entries)
        logs = jira_logs(jira_client, email, ledgertag, '', jira_id)
        for log in logs:
            if log in entries_to_add:
                entries_to_add.remove(log)
            else:
                entries_to_remove.append(log)

    return entries_to_add, entries_to_remove

def sync_ledger_jira(server, email, password, ledgerfile, ledgertag, assocfile, no_delete):
    ticket_mappings = read_ledger_jira_assoc(assocfile)

    all_entries = read_ledger(ledgerfile, [ledgertag])

    jira_client = JIRA(basic_auth=(email, password), server=server)

    entries_to_add, entries_to_remove = determine_adds_and_deletes(jira_client, email, ledgertag, ticket_mappings, all_entries)

    if no_delete:
        entries_to_remove = []

    if not entries_to_remove and not entries_to_add:
        print 'Nothing to do'

    if entries_to_remove:
        print 'I will delete the following entries: '
        for e in entries_to_remove:
            print e

    if entries_to_add:
        print 'I will add the following entries: '
        for e in entries_to_add:
            print e

    if raw_input('Press enter to continue <enter>') != '':
        return

    if entries_to_remove:
        print'Deleting...'
        for entry_to_remove in entries_to_remove:
            entry_to_remove.jira_log.delete()
        print 'Done'

    if entries_to_add:
        print'Adding...'
        for entry_to_add in entries_to_add:
            date = datetime.strptime(entry_to_add.date, '%Y-%m-%d')
            date = datetime(date.year, date.month, date.day, 17, tzinfo=UTC())
            comment = entry_to_add.comment
            jira_client.add_worklog(entry_to_add.jira_id, None, int(entry_to_add.time_spent_seconds), None, None, None, comment, date)
        print 'Done'
