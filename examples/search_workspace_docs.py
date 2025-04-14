from clickup_python_sdk.api import ClickupClient

# Initialize the client
client = ClickupClient.init(user_token="your_user_token_here")

# Get a team/workspace
teams = client.get_teams()
team = teams[0]  # First team

print(team)
# Search for all documents
docs = team.search_docs()

print("All Documents:")
for doc in docs:
    print(f"Document ID: {doc.get('id')}, Name: {doc.get('name')}")
