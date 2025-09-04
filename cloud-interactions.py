import requests

def get_access():
    # Read existing data first
    try:
        with open("session_data/ACCESS.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    headers = {}
    # Parse existing data
    for line in lines:
        line = line.strip()
        if line and ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    # Check for missing values and prompt user if needed
    missing_data = False

    if 'api_key' not in headers or headers['api_key'] == "":
        api_key = input("api_key is missing. Please enter your api_key: ")
        headers['api_key'] = api_key

        # Remove existing empty api_key line if it exists
        lines = [line for line in lines if not line.strip().startswith('api_key:')]
        # Write a new one
        lines.append(f"\napi_key: {api_key}")
        missing_data = True

    if 'workspace_id' not in headers or headers['workspace_id'] == "":
        workspace_id = input("workspace_id is missing. Please enter your workspace_id: ")
        headers['workspace_id'] = workspace_id

        # Remove existing empty workspace_id line if it exists
        lines = [line for line in lines if not line.strip().startswith('workspace_id:')]
        # Write a new one
        lines.append(f"\nworkspace_id: {workspace_id}")
        missing_data = True

    # Write back to file only if new data was added
    if missing_data:
        with open("session_data/ACCESS.txt", "w") as file:
            file.writelines(lines)

    # Return the required headers with proper key names
    return {
        "api-key": headers['api_key'],
        "workspace_id": headers['workspace_id']
    }


def project_get_recordings():
    # Define your credentials and IDs
    # project_id = ""
    project_id = input("Please enter your project_id: ").strip()

    # Set the request headers
    headers = get_access()

    # Get all recordings in the project
    endpoint = f"https://api.cloud.pupil-labs.com/v2/workspaces/{headers['workspace_id']}/projects/{project_id}/recordings/"
    response = requests.get(endpoint, headers=headers)

    # Error handling
    if response.status_code != 200:
        print(f"Failed to retrieve recordings: {response.status_code}")
        print(response.text)
        exit()

    # Parse and print recordings
    recordings = response.json()['result']
    with open('session_data/recordings.txt', 'w') as file:
    #print("Recording ID\t\t\tWearer\t\t\tRecording Name")
    #print("="*70)
    # I didn't need to parse this into a file, but feel free to create a tsv and write the s strings line by line
        for rec in recordings:
            file.write(f"{rec['recording_id']}\n")


def recording_get_events(headers, recording_id: str):
    # Set the request headers
    # headers = get_access()

    # Get all events
    list_endpoint = f"https://api.cloud.pupil-labs.com/v2/workspaces/{headers['workspace_id']}/recordings/{recording_id}/events"
    response = requests.get(list_endpoint, headers=headers)

    # Error handling
    if response.status_code != 200:
        print(f"Failed to retrieve events: {response.status_code}")
        print(response.text)
        exit()

    events = response.json()["result"]
    filtered_events = []
    for e in events:
            filtered_events.append({'id': e['id'], 'name': e['name'], 'offset_s': e['offset_s']})
    return filtered_events

def retrieve_all_events():
    # Define your credentials and IDs
    access_headers = get_access()

    events = {}
    with open("session_data/recordings.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            # Dismiss all empty lines
            recording_id = line.strip()
            if recording_id:
                # Retrieve events for each recording
                events[f'{recording_id}'] = recording_get_events(access_headers, recording_id)
                # For debug - remove if needed
                print(f"LOADING EVENTS OF RECORDING {recording_id}...")

def main():
    project_get_recordings()
    retrieve_all_events()



if __name__ == "__main__":
    main()
