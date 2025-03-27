import requests
import json

# Replace with your ONTAP cluster details
cluster_ip = "192.168.0.101"
username = "admin"
password = "Netapp1!"

# Disable SSL warnings (optional)
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


# Function to get CIFS sessions
def get_cifs_sessions():
    url = f"https://{cluster_ip}/api/protocols/cifs/sessions"
    response = requests.get(url, auth=(username, password), verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Get CIFS sessions data
cifs_sessions = get_cifs_sessions()

if cifs_sessions:
    # Debug: Print the raw data to inspect its structure
    print(json.dumps(cifs_sessions, indent=4))

    # Process the data to find top users
    user_sessions = {}
    for session in cifs_sessions.get("records", []):  # Use .get() to avoid KeyError
        user = session.get('user')  # Safely get the 'user' key
        if user:  # Only process if 'user' exists and is not None
            if user not in user_sessions:
                user_sessions[user] = 0
            user_sessions[user] += 1

    # Sort users by the number of sessions
    top_users = sorted(user_sessions.items(), key=lambda x: x[1], reverse=True)

# Print the top users
print("Top CIFS Users:")
for user, session_count in top_users:
        print(f"User: {user}, Sessions: {session_count}")
else:
    print("No CIFS sessions data found.")
