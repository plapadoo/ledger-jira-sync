# -*- coding: utf-8 -*-
import argparse
from ledger_jira_sync.core import sync_ledger_jira

# Parameter: JIRA-Login-Email, JIRA-Passwort, Ledger-Tag-Nutzername, Pfad zu Assoziationsdatei, Soll gelöscht werden? Default: ja
# Konfigurierbar ob mit Kommentar oder ohne in JIRA gepostet werden soll pro Ticket. Default: Ohne Kommentare

jira_email = 'krinnewitz@plapadoo.de'
ledger_username = 'Kim'

parser = argparse.ArgumentParser(description='Synchronize JIRA and ledger')
parser.add_argument('--server', required=True, help='JIRA server to connect to')
parser.add_argument('--email', required=True, help='JIRA e-mail to use for log-in')
parser.add_argument('--password', required=True, help='JIRA password to use for log-in')
parser.add_argument('--ledgerfile', required=True, help='The ledger file to take accounts from')
parser.add_argument('--ledgertag', required=True, help='Your ledger user-name')
parser.add_argument('--assocfile', required=True, help='Ledger-JIRA association file')
parser.add_argument('--nodelete', action='store_const', const=True, help='Whether to delete entries or only add them')

def main(args=None):
    args = parser.parse_args()
    sync_ledger_jira(args.server, args.email, args.password, args.ledgerfile, args.ledgertag, args.assocfile, args.nodelete)

if __name__ == "__main__":
    main()
