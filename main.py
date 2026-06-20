"""Computer Companion."""
import json
import os

DEFAULT_APPS = {"Powershell": "powershell",
                "Command Prompt": "cmd",
                "Cmd": "cmd",
                "Settings": "ms-settings:",
                "Device Manager": "devmgmt.msc",
                "DVM": "devmgmt.msc",
                "Task Manager": "taskmgr",
                "TM": "taskmgr"}
request = ""


def file_setup():
    """Do a check if .json file exists, and if not creates them."""
    if not os.path.exists("data/first.json"):
        with open("data/first.json", "w") as f:
            json.dump(0, f)
    if not os.path.exists("data/name.json"):
        with open("data/name.json", "w") as f:
            json.dump("", f)


file_setup()
# Loads .json files for data into variables
with open("data/first.json", "r") as f:
    returning = json.load(f)
with open("data/name.json", "r") as f:
    name = json.load(f)


def welcome_first():
    """Do greeting for first time user."""
    print("Welcome to Computer Companion!")
    name = input("Please enter your name: ")
    with open("data/first.json", "w") as f:
        json.dump(1, f)
    with open("data/name.json", "w") as f:
        json.dump(name, f)
    print(f"Nice to meet you, {name}!")


def welcome_returning(name):
    """Do greeting for returning user."""
    print(f"Welcome Back, {name}!")


def app_opener():
    """Do the app opening function."""
    print(f"App options: {', '.join(DEFAULT_APPS)}")
    app_name = input("What app would you like to open? ").lower()
    for key, value in DEFAULT_APPS.items():
        if app_name == key.lower():
            os.startfile(value)
            print(f"Opening {value}...")
            return
    print("App not found.")


"""Actual program starts here."""
if returning == 1:
    welcome_returning(name)
else:
    welcome_first()

while request != "exit" and request != "quit":
    print("Functions: O - Open an app, Exit - Exit the program, "
          "Help - Help menu")
    request = input("What would you like to do? ").lower()
    if request == "o":
        app_opener()
