# simple-todo-cli-application
A straightforward CLI application designed to efficiently manage notes and memos directly from the terminal. This tool fills a notable gap in standard terminal functionalities, providing a streamlined and convenient way to handle your tasks and reminders without leaving the command line interface.



# Todo CLI Application

## Overview

This CLI (Command-Line Interface) application is a simple yet powerful tool to manage your todo notes. It allows you to create, read, update, and delete todos with different priorities. You can also manage multiple save files, making it easy to organize your tasks.

## Features

- **Create Todos**: Add new todo notes with a name, description, priority, and optional date.
- **Read Todos**: Display todos by index or name. You can also view all todos in a list.
- **Update Todos**: Modify existing todos by index or name.
- **Delete Todos**: Remove todos by index.
- **Save Management**: Create, rename, delete, and list save files. You can also set an active save file.
- **Priority Levels**: Assign priorities to your todos (Low, Medium, High) and see them color-coded in the output.

## Installation

### Prerequisites

- **Python 3.x**: Ensure that Python is installed on your machine. You can download it from [python.org](https://www.python.org/).

### Steps

1. **Clone the Repository**:  
   If you have Git installed, you can clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/todo-cli.git
   cd todo-cli




Todo CLI Application
Overview
This CLI (Command-Line Interface) application is a simple yet powerful tool to manage your todo notes. It allows you to create, read, update, and delete todos with different priorities. You can also manage multiple save files, making it easy to organize your tasks.

Features
Create Todos: Add new todo notes with a name, description, priority, and optional date.
Read Todos: Display todos by index or name. You can also view all todos in a list.
Update Todos: Modify existing todos by index or name.
Delete Todos: Remove todos by index.
Save Management: Create, rename, delete, and list save files. You can also set an active save file.
Priority Levels: Assign priorities to your todos (Low, Medium, High) and see them color-coded in the output.
Installation
Prerequisites
Python 3.x: Ensure that Python is installed on your machine. You can download it from python.org.
Steps
Clone the Repository:
If you have Git installed, you can clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/todo-cli.git
cd todo-cli
Alternatively, you can download the source code as a ZIP file from the repository and extract it to a directory of your choice.

Install Dependencies:
This application uses the Click package to build the CLI. You can install it using pip:

bash
Copy code
pip install click tabulate
Make the Script Executable (Optional):
To make the script easier to run, you can add executable permissions:

bash
Copy code
chmod +x todo_cli.py
Then, you can run the script directly:

bash
Copy code
./todo_cli.py
Alternatively, you can run it with Python:

bash
Copy code
python todo_cli.py
Usage
Once installed, you can start managing your todos by running the CLI commands.

Commands Overview
Creating a Todo

bash
Copy code
python todo_cli.py create-todo
Follow the prompts to enter the todo name, description, priority, and date.

Reading a Todo by Index

bash
Copy code
python todo_cli.py read-todo <index>
Replace <index> with the index of the todo you want to read.

Reading a Todo by Name

bash
Copy code
python todo_cli.py read-todo-by-name <name>
Replace <name> with the name of the todo you want to read.

Reading All Todos

python todo_cli.py read-all
Updating a Todo by Index

python todo_cli.py update-todo <index>
Replace <index> with the index of the todo you want to update.

Updating a Todo by Name

python todo_cli.py update-todo-by-name <name>
Replace <name> with the name of the todo you want to update.

Deleting a Todo by Index

bash
Copy code
python todo_cli.py delete-todo <index>
Replace <index> with the index of the todo you want to delete.

Saving Todos

bash
Copy code
python todo_cli.py save-todo
Creating a New Save File

bash
Copy code
python todo_cli.py create-save-file <filename>
Replace <filename> with the name of the new save file.

Listing All Save Files

bash
Copy code
python todo_cli.py list-files
Setting an Active Save File

bash
Copy code
python todo_cli.py set-active <index>
Replace <index> with the index of the save file you want to set as active.

Renaming a Save File

bash
Copy code
python todo_cli.py rename-file <old_filename> <new_filename>
Replace <old_filename> and <new_filename> with the old and new names of the save file.

Deleting a Save File

bash
Copy code
python todo_cli.py delete-file <filename>
Replace <filename> with the name of the save file you want to delete.

Example Workflow
Create a Todo:

bash
Copy code
python todo_cli.py create-todo
Follow the prompts to enter the details of the todo.

Read All Todos:

bash
Copy code
python todo_cli.py read-all
This will list all the todos you have created.

Update a Todo:

bash
Copy code
python todo_cli.py update-todo 1
This will update the todo at index 1.

Save the Todo List:

bash
Copy code
python todo_cli.py save-todo
Create a New Save File:

bash
Copy code
python todo_cli.py create-save-file my_tasks.json
Set Active Save File:

bash
Copy code
python todo_cli.py set-active 1
Directory Structure
The application stores all data in a hidden directory under your home directory (~/.todo_cli). The structure is as follows:

javascript
Copy code
~/.todo_cli/
    ├── saves/
    │   ├── default_save.json
    │   └── my_tasks.json
    └── settings.json
saves/: Contains all the save files.
settings.json: Contains the settings, including the active save file.
Contributing
Contributions are welcome! If you find any bugs or have feature requests, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License.

