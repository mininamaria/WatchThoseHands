import requests
import typing
import os

# This will be moved to a separate file for security reasons
def authenticate():
    print("Authentification...")
    if not os.path.exists("ACCESS.txt"):
        print(f"File ACCESS.txt not found.")
        return
    with open("ACCESS.txt", "r") as f:
        workspace_id = f.readline().split(sep=":")[1].strip()
        api_key = f.readline().split(sep=":")[1].strip()
        headers = {
            "api-key": api_key,
            "workspace_id": workspace_id,
        }
    return headers

#"kLP22bXM3ekj7MUVmo36T7erup5hDMfdwuwHGg5ozymR"


#payload = {"name": "test_1", "offset_s": 61.230}

def collect_timestamps(wearer: str, view: str, recording_id: str, headers: typing.Dict[str, str]):
    if not os.path.exists(f"timestamps/{wearer}-view_{view}.tsv"):
        print(f"File timestamps/{wearer}-view_{view}.tsv not found.")
        return
    with open(f"timestamps/{wearer}-view_{view}.tsv", "r") as timestamps_file:
        timestamps_file.readline()
        print(f"Reading timestamps from {wearer}-view_{view}.tsv...\n")
        for line in timestamps_file:
            seconds, timestamp, event = line.strip().split("\t")
            payload = create_payload(event, seconds)
            extrastr = f"timestamp: {seconds}\tevent: {event}"
            #dummy_send_event_creation_request(payload=payload, message=extrastr, recording_id=recording_id)
            send_event_creation_request(payload=payload, recording_id=recording_id, headers=headers)

def create_payload(event_name: str, offset_s: str):
    return {'name': event_name, 'offset_s': offset_s}


def send_event_creation_request(headers: typing.Dict, recording_id: str, payload: typing.Dict):
    endpoint = (
        f"https://api.cloud.pupil-labs.com/v2/workspaces/{headers["workspace_id"]}/recordings/{recording_id}/events"
    )
    response = requests.request("POST", endpoint, json=payload, headers=headers)
    #print(f"Status: {response.status_code}, Response: {response.text}")
    if not response.ok:
        raise Exception(f"Failed to create event: {response.status_code} - {response.text}")


def dummy_send_event_creation_request(recording_id: str, payload: typing.Dict, message: str = ""):
    endpoint = (
        f"https://api.cloud.pupil-labs.com/v2/workspaces/HSE/recordings/{recording_id}/events"
    )
    print("POST NEW REQUEST-------\n "
          f"for {message}\n"
          f"---endpoint: {endpoint}\n"
          f"---payload: {payload}\n")

def main():
    tokens = authenticate()
    session_wearer = input("Enter session wearer: ")
    session_view = input("Enter session view: ")
    recording_id = input("Enter recording ID: ")
    collect_timestamps(wearer=session_wearer, view=session_view, recording_id=recording_id, headers=tokens)
    #pld = create_payload()
    #send_event_creation_request(pld)

if __name__ == "__main__":
    main()
