"""Computer Companion."""
import json
import os
import sys
import time

try:
    from pythonping import ping
except ImportError:
    print("To use ping utilities, you need to install the pythonping "
    "library. \nPlease run: pip install pythonping in your terminal.")
DEFAULT_APPS = {"Powershell": "powershell",
                "Command Prompt": "cmd",
                "Cmd": "cmd",
                "Settings": "ms-settings:",
                "Device Manager": "devmgmt.msc",
                "DVM": "devmgmt.msc",
                "Task Manager": "taskmgr",
                "TM": "taskmgr"}
request = ""
ping_ip = []

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
    print(f"Nice to meet you, {name}!\n")


def welcome_returning(name):
    """Do greeting for returning user."""
    print(f"Welcome Back, {name}!\n")


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

def ping_utility():
    import ipaddress

    valid_ip_count = False
    valid_ping_count = False
    while not valid_ip_count:
        ping_ip_counts = input("How many IP Addresses would you like to ping simultaneously? ")
        try:
            ping_ip_counts = int(ping_ip_counts)
            if ping_ip_counts < 1 or ping_ip_counts > 32:
                print("Please enter a number greater than 0 and less than or equal to 32.")
            else:
                valid_ip_count = True
        except ValueError:
            print("Please enter a valid number.")

    while not valid_ping_count:
        ping_times = input("How many times should I ping? ")
        try:
            ping_times = int(ping_times)
            if ping_times < 1 or ping_times > 200:
                print("Please enter a number greater than 0 and less than or equal to 200.")
            else:
                valid_ping_count = True
        except ValueError:
            print("Please enter a valid number.")

    ips = []
    for i in range(ping_ip_counts):
        while True:
            addr = input(f"Please enter IP Address {i + 1}: ")
            try:
                ipaddress.IPv4Address(addr)
                ips.append(addr)
                break
            except ipaddress.AddressValueError:
                print("Invalid IPv4 address. Please enter a valid IP address.")

    for _ in range(ping_times):
        time.sleep(1)
        for addr in ips:
            try:
                response = ping(addr, count=1, verbose=False)
                if response.success():
                    print(f"\033[32m\n{addr} is online!\033[0m")
                else:
                    print(f"\033[31m\n{addr} is offline.\033[0m")
            except PermissionError:
                print("\n[ERROR] Pure Python ping requires Administrator/Root privileges.")
                print("Please run this terminal/script as Administrator.")
                return
            except RuntimeError:
                print(f"\n[ERROR] Could not ping {addr}. Please check the IP address and try again.")
                continue


def utilities():
    """Display other utilities."""
    utility_request = ""
    while utility_request != "clear":
        print("Utilities: Clear - Clear the chat, C - Calculator, F - Fun, "
            "R - Random Generators, S - System Info, P - Ping")
        utility_request = input("Which utility would you like to use? ").lower()
        if utility_request == "p":
            ping_utility()


"""Actual program starts here."""
if returning == 1:
    welcome_returning(name)
else:
    welcome_first()

while request != "exit" and request != "quit":
    print("Functions: O - Open an app, Exit - Exit the program, "
          "U - Other Utilities, Help - Help menu")
    request = input("What would you like to do? ").lower()
    if request == "o":
        app_opener()
    elif request == "u":
        utilities()
    elif request == "help":
        print("You asked for help, and I will provide!"
              "I am your computer companion. Tell me a"
              " command, and I will do it. Here "
              "are the commands you can use: "
              "Functions: O - Open an app, Exit - Exit the program, "
              "U - Other Utilities, Help - Help menu")
    elif request == "exit" or request == "quit":
        print("Goodbye!")
    else:
        print("That is not a valid command. Please try again.")
