from clickup_python_sdk.api import ClickupClient
from clickup_python_sdk.clickupobjects.document import Document
from clickup_python_sdk.clickupobjects.documentpage import DocumentPage

# Initialize the client with your ClickUp API token
client = ClickupClient.init(user_token="your_user_token_here")

# Get the first workspace
team = client.get_teams()[1]
workspace_id = team["id"]

# Search for documents in the workspace
docs = team.search_docs()
if not docs:
    print("No documents found.")
    exit()

# Get the first document
doc = docs[0]
doc.get()  # Fetch full document details
print(f"Document: {doc['name']}")  # Access name from document data

# Get all pages in the document
pages = doc.get_pages()
print(f"\nFound {len(pages)} pages")

# Create a new page
new_page = doc.create_page(
    name="My New Page",
    content="# Hello World\n\nThis is my new page",
    sub_title="A subtitle",
)
print(f"\nCreated new page: {new_page['name']}")

# Update the page
updated_page = new_page.update(
    name="Updated Page Name", content="# Updated Content\n\nThis is the updated content"
)
print(f"Updated page: {updated_page['name']}")

# Get a specific page by ID
page = DocumentPage(id=new_page["id"], workspace_id=workspace_id, doc_id=doc["id"])
page.get()
print(f"\nPage content: {page['content']}")
