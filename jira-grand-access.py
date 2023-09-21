import csv
import json
import requests

# Load Jira configuration
with open('jira_config.json', 'r') as config_file:
    jira_config = json.load(config_file)


def create_jira_ticket(data, ticket_number):
    url = f"{jira_config['jira_url']}/rest/servicedeskapi/request"
    headers = {
        'Content-Type': 'application/json',
    }
    auth = (jira_config['username'], jira_config['password'])

    summary = f"[TEST]wd recruiter mass ticket# {ticket_number}"
    dynamic_fields = {
        "customfield_12647": data[0],
        "customfield_11763": [{"id": "12590"}] if data[1] == "1" else [],
        "customfield_10150": [{"id":"10412"},{"id": "16064"}] if data[1] == "1" else [{"id": "16064"}],
        "customfield_12548": "" if data[1] == "1" else data[0],
        "customfield_10089": data[2],
        "customfield_10090": data[3],
        "customfield_12040": data[4],
#        "customfield_12543": data[5], this is responsible person. skipped for now
        "customfield_10622": data[6],
        "customfield_10191": {"id": "16208"},
        "customfield_12573": {"id": "16195"}

    }

    payload = {
        "serviceDeskId": jira_config['serviceDeskId'],
        "requestTypeId": jira_config['requestTypeId'],
        "requestFieldValues": {
            "summary": summary,
            "customfield_12634": "2023-12-30",
            **dynamic_fields
        }
    }

    print(f"Sending request for Ticket {ticket_number}:")
    print(json.dumps(payload, indent=4))  # Print the request payload before sending

    response = requests.post(url, headers=headers, auth=auth, json=payload)

    if response.status_code == 201:
        ticket_data = response.json()
        ticket_id = ticket_data.get('issueKey')
        print(f"Ticket {ticket_number} created successfully. Ticket ID: {ticket_id}")
    else:
        print(f"Error creating ticket {ticket_number}. Status code: {response.status_code}, Response: {response.text}")


# Read data from CSV
with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header
    for i, row in enumerate(csv_reader, 1):
        create_jira_ticket(row, i)
