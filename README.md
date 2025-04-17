# ClickUp Python SDK

## Introduction

The ClickUp Python SDK is a comprehensive wrapper for the ClickUp API (v2), designed to simplify interactions with ClickUp for Python developers. This SDK helps businesses automate their ClickUp workflows and integrate ClickUp data with other systems.

## Installation

### From PyPI (Coming Soon)

```bash
pip install clickup-python-sdk
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/clickup-python-sdk.git

# Navigate to the project directory
cd clickup-python-sdk

# Install the package in development mode
pip install -e .
```

## Package Structure

```
clickup-python-sdk/
├── LICENSE.txt
├── README.md
├── setup.py
├── requirements.txt
├── clickup_python_sdk/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   └── clickupobjects/
│       ├── __init__.py
│       ├── abstractobject.py
│       ├── checklist.py
│       ├── checklistitem.py
│       ├── comment.py
│       ├── customfield.py
│       ├── dependency.py
│       ├── document.py
│       ├── folder.py
│       ├── group.py
│       ├── list.py
│       ├── space.py
│       ├── tags.py
│       ├── task.py
│       ├── tasktemplate.py
│       ├── team.py
│       ├── timeentry.py
│       ├── user.py
│       └── view.py
├── examples/
│   └── search_workspace_docs.py
└── tests/
    └── __init__.py
```

## Authentication

Initialize the client with your ClickUp API token:

```python
from clickup_python_sdk import ClickupClient

# Initialize the client
client = ClickupClient.init(user_token="your_clickup_api_token")
```

## Features

- **Teams/Workspaces**: Access workspace data and manage spaces
- **Spaces**: Manage spaces, lists, and tags
- **Folders**: Access and manage folders within spaces
- **Lists**: Create and manage tasks within lists
- **Tasks**: Create, update, delete, and manage tasks
- **Documents**: Search and manage documents within workspaces
- **Custom Fields**: Work with custom fields on tasks
- **Comments**: Add, update, and delete comments on tasks
- **Checklists**: Create and manage checklists within tasks
- **Time Tracking**: Track time spent on tasks
- **Dependencies**: Manage task dependencies
- **Groups**: Manage user groups within workspaces

## Usage Examples

### Getting Teams/Workspaces

```python
# Get all workspaces the authenticated user belongs to
teams = client.get_teams()
```

### Accessing Spaces in a Workspace

```python
# Get a list of spaces for a workspace
team = teams[0]  # First workspace
spaces = team.get_spaces()
```

### Working with Lists

```python
# Get lists in a space
space = spaces[0]  # First space
lists = space.get_lists()

# Access a specific list
task_list = lists[0]  # First list
```

### Creating a Task

```python
# Create a new task in a list
new_task = task_list.create_task(
    name="New Task",
    description="Task description",
    status="Open",
    priority=3,  # 1 is highest, 4 is lowest
    due_date=1649887200000  # Timestamp in milliseconds
)
```

### Updating a Task

```python
# Update an existing task
task = client.get_task(task_id="task_id_here")
task.update(
    name="Updated Task Name",
    status="In Progress"
)
```

### Searching for Documents

```python
# Search for documents in a workspace
team = teams[0]  # First workspace
docs = team.search_docs()

# Search with filters
filtered_docs = team.search_docs(
    creator=12345,          # Documents created by user with ID 12345
    archived=False,         # Non-archived documents
    parent_type="SPACE",    # Documents that are children of a space
    limit=20                # Return up to 20 results
)

# Get a specific document by ID
specific_docs = team.search_docs(doc_id="doc_id_here")
if specific_docs:
    doc = specific_docs[0]
    doc_details = doc.get()  # Get full document details
```

### Working with Custom Fields

```python
# Get custom fields for a list
custom_fields = task_list.get_custom_fields()

# Update a task's custom field
task = client.get_task(task_id="task_id_here")
task.update_custom_field(
    custom_field_id="custom_field_id",
    value="new_value"
)
```

## Running Examples

You can run the provided examples to see the SDK in action:

```bash
# Run the document search example
python examples/search_workspace_docs.py
```

## Object Types

The SDK provides object-oriented interfaces for ClickUp's core components:

- `Team`: Team/Workspace management
- `Space`: Space operations within workspaces
- `Folder`: Folder management within spaces
- `List`: Task list operations
- `Task`: Task operations and management
- `Document`: Document operations and management
- `CustomField`: Custom field functionality
- `User`: User information
- `Tag`: Tag management
- `Comment`: Comment operations
- `Checklist/ChecklistItem`: Checklist operations
- `TimeEntry`: Time tracking operations
- `Dependency`: Task dependency management

## Error Handling

The SDK includes built-in error handling for API responses. Failed requests will raise exceptions with appropriate error messages from the ClickUp API.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE.txt file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions or issues, please open an issue on the repository.

## Object Initialization and Retrieval

Most objects in the SDK can be initialized with just an ID and then retrieved using the `get()` method. However, some objects require additional context IDs for initialization.

### Basic Object Initialization

Here's how to initialize and retrieve a Task object:

```python
# Initialize with just the ID
task = Task(id="task_id_here")

# Get full task details
task.get()
```

### Objects Requiring Additional Context

Some objects require additional context IDs for initialization. Here are examples:

1. Document objects require workspace_id:

```python
# Initialize with required workspace_id
doc = Document(id="document_id", workspace_id="team_id")
doc.get()
```

2. DocumentPage objects require both workspace_id and doc_id:

```python
# Initialize with required IDs
page = DocumentPage(
    id="page_id",
    workspace_id="team_id",
    doc_id="document_id"
)
page.get()
```

3. Objects from Team search (automatic context):

```python
# Get documents from a team (workspace_id is automatically set)
team = client.get_teams()[0]
docs = team.search_docs()
doc = docs[0]
doc.get()
```

The `get()` method will retrieve the complete object details from the ClickUp API and update the object with the latest information. Check the documentation for each object type to understand its specific initialization requirements.
