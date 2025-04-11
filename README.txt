# ClickUp Python SDK

## Introduction
The ClickUp Python SDK is a comprehensive wrapper for the ClickUp API (v2), designed to simplify interactions with ClickUp for Python developers. This SDK helps businesses automate their ClickUp workflows and integrate ClickUp data with other systems.

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/clickup_python_sdk.git

# Install dependencies
pip install -r requirements.txt
```

## Authentication
Initialize the client with your ClickUp API token:

```python
from clickup_python_sdk.api import ClickupClient

# Initialize the client
client = ClickupClient.init(user_token="your_clickup_api_token")
```

## Features
- **Teams**: Access team data and spaces
- **Spaces**: Manage spaces, lists, and tags
- **Folders**: Access and manage folders within spaces
- **Lists**: Create and manage tasks within lists
- **Tasks**: Create, update, delete, and manage tasks
- **Custom Fields**: Work with custom fields on tasks

## Usage Examples

### Getting Teams
```python
# Get all teams the authenticated user belongs to
teams = client.get_teams()
```

### Accessing Spaces in a Team
```python
# Get a list of spaces for a team
team = teams[0]  # First team
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
new_task = task_list.create_task({
    "name": "New Task",
    "description": "Task description",
    "status": "Open",
    "priority": 3,  # 1 is highest, 4 is lowest
    "due_date": 1649887200000  # Timestamp in milliseconds
})
```

### Updating a Task
```python
# Update an existing task
task = client.get_task(task_id="task_id_here")
task.update({
    "name": "Updated Task Name",
    "status": "In Progress"
})
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

## Object Types
The SDK provides object-oriented interfaces for ClickUp's core components:
- `Team`: Team management
- `Space`: Space operations within teams
- `Folder`: Folder management within spaces
- `List`: Task list operations
- `Task`: Task operations and management
- `CustomField`: Custom field functionality
- `User`: User information
- `Tag`: Tag management

## Error Handling
The SDK includes built-in error handling for API responses. Failed requests will raise exceptions with appropriate error messages from the ClickUp API.

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE.txt file for details.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Support
For questions or issues, please open an issue on the repository.
