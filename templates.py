"""
Author: Aditya Bhatt
Date: 10:08 AM 30-08-2024

NOTE: This file helps create the necessary structure for a Flask project within the existing project folder.

TODO:

BUG :
"""
import os

def create_file(file_path, content=""):
    """
    Creates a file with the specified content if it does not already exist.

    Args:
        file_path (str): The path of the file to be created.
        content (str): The content to be written to the file.
    """
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

def create_directory(directory_path):
    """
    Creates a directory if it does not already exist.

    Args:
        directory_path (str): The path of the directory to be created.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")

def create_flask_project():
    """
    Creates the essential files and directories for a Flask project.
    """
    project_dir = os.getcwd()

    # Create necessary directories
    create_directory(os.path.join(project_dir, "static"))
    create_directory(os.path.join(project_dir, "templates"))
    create_directory(os.path.join(project_dir, "src"))
    create_directory(os.path.join(project_dir,"tests"))

    # Create necessary files
    create_file(os.path.join(project_dir,"requirements.txt"))
    create_file(os.path.join(project_dir, ".env"))
    # create_file(os.path.join(project_dir,".gitignore"))
    create_file(os.path.join(project_dir,"setup.sh"))
    # create_file(os.path.join(project_dir,"README.md"))
    create_file(os.path.join(project_dir, "app.py"), content="""
from flask import Flask

app = Flask(__name__)

# Add your routes and logic here

if __name__ == "__main__":
    app.run(debug=True)
    """)

    print(f"Flask project structure checked and updated in: {project_dir}")

if __name__ == "__main__":
    create_flask_project()
