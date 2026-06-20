"""Computer Companion."""
import json
import os

if not os.path.exists("data/first.json"):
    with open("data/first.json", "w") as f:
        json.dump({}, f)

with open("data/first.json", "r") as f:
    returning = json.load(f)


DEFAULT_APPS = ["Powershell", "Command Prompt", "Settings",
                "Device Manager", "Task Manager"]

def welcome_first():
    """Do greeting for first time user."""
    print("Welcome to Computer Companion!")


def welcome_returning():
    """Do greeting for returning user."""
    print("Welcome Back!")


if returning == 1:
    welcome_returning()
else:
    welcome_first()
    with open("data/first.json", "w") as f:
        json.dump(1, f)
