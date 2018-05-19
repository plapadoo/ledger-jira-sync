import ledger
from ledger_jira_sync.ledger_entry import LedgerEntry


def read_ledger(filename, authors):
    journal = ledger.read_journal(filename)

    result = []

    for xact in journal.xacts():
        date = xact.date
        if hasattr(xact, 'note'):
            comment = xact.note
        else:
            comment = None

        for post in xact.posts():
            amount = post.amount

            if amount <= 0:
                continue

            author = None
            for test_author in authors:
                if post.has_tag(test_author):
                    author = test_author

            if author is None:
                continue
                # raise Exception('line '+str(post.pos.beg_line)+': post without author found')

            account = post.account

            # conversion to str for date: it's datetime.date otherwise
            result.append(LedgerEntry(int(amount), author, str(date), account, comment))
    return result
