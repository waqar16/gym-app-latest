import os
import sys
import subprocess

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "membership_system.settings")

    # Get the path to the manage.py file relative to the current directory
    manage_py_path = (r"D:\CodeNexo\gymapp\membership_system\manage.py")

    sys.argv.extend(["runserver", "0.0.0.0:8000", "--noreload"])

    # Run the Django server with the correct path to manage.py
    subprocess.run(["cmd.exe", "/K", "python", manage_py_path] + sys.argv[1:])
