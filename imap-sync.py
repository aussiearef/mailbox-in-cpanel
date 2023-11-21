# mailbox information is located in mailbox_passwords.csv
# the three columns or fields in each row of the above csv file are mailbox, old_password, new_password

import csv
import imaplib
import email  # uses requests library. run pip install requests 
from email.message import Message
from email import policy
from email.parser import BytesParser

SOURCE_SERVER="" # source imap server
DEST_SERVER="" # destination imap server

def copy_emails(source_server, source_mailbox, source_password, destination_server, destination_mailbox, destination_password):

    source_conn = imaplib.IMAP4_SSL(source_server)
    source_conn.login(source_mailbox, source_password)

    dest_conn = imaplib.IMAP4_SSL(destination_server)
    dest_conn.login(destination_mailbox, destination_password)

    source_conn.select(mailbox=source_mailbox, readonly=True)

    _, source_data = source_conn.uid('SEARCH', None, 'ALL')
    uids = source_data[0].split()

    for uid in uids:
        _, msg_data = source_conn.uid('FETCH', uid, '(RFC822)')
        msg_bytes = msg_data[0][1]
        msg = BytesParser(policy=policy.default).parsebytes(msg_bytes)

        dest_conn.append(destination_mailbox, None, None, msg_bytes)

    source_conn.close()
    dest_conn.close()

    source_conn.logout()
    dest_conn.logout()

def main():

    with open('mailbox_passwords.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  

        for row in csv_reader:
            mailbox, old_password, new_password = row

            source_mailbox = "inbox"
            destination_mailbox = "inbox"

            try:
                copy_emails(SOURCE_SERVER, source_mailbox, old_password, DEST_SERVER, destination_mailbox, new_password)
                print(f"Emails copied successfully for {mailbox}")
            except Exception as e:
                print(f"Failed to copy emails for {mailbox}: {str(e)}")

if __name__ == "__main__":
    main()
