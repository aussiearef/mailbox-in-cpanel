# cpanel-accounts.csv file includes cpanel accounts. 
# each row in cpanel-accounts.csv includes cpanel_account, cpanel_password

# cpanel-accounts.csv file includes mailbox information. 
# each row in cpanel-accounts.csv includes mailbox_cpanel_account, email, password

# cpanel url, usernam and password must be set below as well.

import requests #pip install requests
import csv

# Replace these with  cPanel details
CPANEL_URL = "https://your-cpanel-domain.com:2083"

def create_mailbox(cpanel_user, email, password, domain):
    api_url = f"{CPANEL_URL}/json-api/cpanel"
    api_params = {
        'cpanel_jsonapi_user': cpanel_user,
        'cpanel_jsonapi_module': 'Email',
        'cpanel_jsonapi_func': 'addpop',
        'cpanel_jsonapi_apiversion': '2',
        'domain': domain,
        'email': email,
        'password': password,
        'quota': 0  
    }

    response = requests.post(api_url, data=api_params, auth=(cpanel_user, password))

    if response.status_code == 200:
        result = response.json()
        if result.get('cpanelresult', {}).get('data', {}).get('status') == 1:
            print(f"Mailbox created successfully for {email}")
        else:
            print(f"Failed to create mailbox for {email}: {result.get('cpanelresult', {}).get('data', {}).get('statusmsg')}")
    else:
        print(f"Failed to create mailbox for {email}. HTTP Status Code: {response.status_code}")

def main():
    # Read cPanel accounts from CSV
    with open('cpanel-accounts.csv', 'r') as cpanel_file:
        cpanel_reader = csv.reader(cpanel_file)
        next(cpanel_reader)  # Skip header row if present

        # Iterate through each cPanel account in the cPanel accounts CSV
        for cpanel_row in cpanel_reader:
            cpanel_account, cpanel_password = cpanel_row

            # Read mailbox information from CSV
            with open('mailboxes.csv', 'r') as mailbox_file:
                mailbox_reader = csv.reader(mailbox_file)
                next(mailbox_reader)  # Skip header row if present

                # Iterate through each row in the mailbox CSV
                for row in mailbox_reader:
                    mailbox_cpanel_account, email, password = row

                    # Check if cPanel account matches
                    if cpanel_account == mailbox_cpanel_account:
                        # Assuming the cpanel_account is the domain in this case
                        create_mailbox(cpanel_account, email, password, cpanel_account)

if __name__ == "__main__":
    main()
