"""Computer Companion."""
import json
import os
import sys
import time
import ipaddress
import random
import platform
import psutil

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def file_setup():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def safe_load_json(path, default):
    """Load JSON from file, or create with default if missing/corrupted."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w") as f:
            json.dump(default, f)
        return default
    
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(path, "w") as f:
            json.dump(default, f)
        return default


file_setup()

returning = safe_load_json(os.path.join(DATA_DIR, "first.json"), 0)
name = safe_load_json(os.path.join(DATA_DIR, "name.json"), "")


def welcome_first():
    print(f"\033[32m\nWelcome to Computer Companion!\033[0m")
    name = input("Please enter your name: ")
    with open(os.path.join(DATA_DIR, "first.json"), "w") as f:
        json.dump(1, f)

    with open(os.path.join(DATA_DIR, "name.json"), "w") as f:
        json.dump(name, f)
    print(f"\033[32mNice to meet you, {name}!\n\033[0m")


def welcome_returning(name):
    WELCOME_MESSAGES = [f"Welcome back, {name}!", f"Hello again, {name}!", 
                    f"Good to see you again, {name}!", f"Welcome back, "
                    f"{name}!",
                    f"Hey {name}, welcome back!", f"A great day to "
                    f"chat with you, {name}!", f"Nice to see you, {name}!"]
    """Do greeting for returning user."""
    print(f"\033[32m\n{WELCOME_MESSAGES[random.randint(0, len(WELCOME_MESSAGES) - 1)]}\033[0m")


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

def calculator():
    """Do the calculator utility."""
    print("\nCalculator")
    print("Select an operator. So far I can only do"
          "addition, subtraction, multiplication, and division, but more"
          "will be added in the future!")
    operator = input("What function do you want to use? (A - Add, "
                    "S - Subtract, M - Multiply, D - Divide) ").lower()
    if operator == "a":
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        print(f"The answer is: {num1 + num2}")
    elif operator == "s":
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        print(f"The answer is: {num1 - num2}")
    elif operator == "m":
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        print(f"The answer is: {num1 * num2}")
    elif operator == "d":
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        if num2 == 0:
            print("Cannot divide by zero.")
        else:
            print(f"The answer is: {num1 / num2}")


def fun():
    """Do the fun utility."""
    JOKES = ["Why don't eggs tell jokes? They'd crack each other up.", "I used to be a baker, but I couldn't make enough dough.", "I’m reading a book on anti‑gravity. It’s impossible to put down.", "Why did the scarecrow win an award? He was outstanding in his field.", "I don't trust stairs. They're always up to something.", "Why did the bicycle fall over? It was two‑tired.", "I used to play piano by ear, now I use my hands.", "Why can't you give Elsa a balloon? She’ll let it go.", "What do you call fake spaghetti? An impasta.", "Why did the math book look sad? Too many problems.", "I’m on a seafood diet. I see food and I eat it.", "Why don’t skeletons fight? They don’t have the guts.", "What do you call cheese that isn’t yours? Nacho cheese.", "Why did the golfer bring two pairs of pants? In case he got a hole in one.", "I used to be addicted to soap, but I’m clean now.", "Why did the tomato blush? It saw the salad dressing.", "What do you call a belt made of watches? A waist of time.", "Why don’t oysters donate to charity? They’re shellfish.", "I told my computer I needed a break, and it said 'No problem — I’ll go to sleep.'", "Why did the cookie go to the doctor? It felt crumby.", "What do you call a factory that makes OK products? A satisfactory.", "Why was the broom late? It swept in.", "Why did the coffee file a police report? It got mugged.", "I used to be a banker, but I lost interest.", "Why don’t crabs share? Because they’re shellfish.", "What do you call a sleeping bull? A bulldozer.", "Why did the chicken join a band? It had drumsticks.", "Why can’t a nose be 12 inches long? Then it’d be a foot.", "What do you call a pile of cats? A meow‑tain.", "Why did the stadium get hot? All the fans left.", "Why did the computer go to therapy? Too many tabs open.", "Why don’t melons get married? They cantaloupe.", "What do you call a fish wearing a bowtie? Sofishticated.", "Why did the man fall into the well? He couldn’t see that well.", "Why don’t vampires go to barbecues? They don’t like stakes.", "What do you call a dog magician? A labracadabrador.", "Why did the orange stop? It ran out of juice.", "Why did the photo go to jail? It was framed.", "Why did the tree get online? To log in.", "Why did the barber win the race? He took a shortcut.", "Why don’t cows have money? Farmers milk them dry.", "Why did the banana go to the doctor? It wasn’t peeling well.", "What do you call a bear with no teeth? A gummy bear.", "Why did the music teacher go to jail? She got caught with too many notes.", "Why did the fish blush? It saw the ocean’s bottom.", "Why don’t seagulls fly over the bay? Then they’d be bagels.", "Why did the calendar get nervous? Its days were numbered.", "Why did the grape stop in the middle of the road? It ran out of juice.", "Why did the belt get arrested? It held up a pair of pants.", "Why did the mushroom get invited to the party? He was a fungi.", "Why did the shovel get promoted? It was outstanding in its field.", "Why did the light bulb fail school? It wasn’t too bright.", "Why did the cow become an astronaut? To see the moooon.", "Why did the frog take the bus? His car got toad.", "Why did the cookie cry? Its mom was a wafer too long.", "Why did the lettuce win the race? It was ahead.", "Why did the pencil cross the road? It had a point.", "Why did the phone wear glasses? It lost its contacts.", "Why did the fridge blush? It saw the salad dressing.", "Why did the bee get married? He found his honey.", "Why did the clock get kicked out of class? It tocked too much.", "Why did the potato sit down? It was a little fried.", "Why did the book join the police? It had too many stories.", "Why did the candle apply for a job? It wanted to make scents.", "Why did the cloud stay home? It was feeling under the weather.", "Why did the keyboard break up with the mouse? It felt clicked on too much.", "Why did the sandwich go to the gym? To get breader.", "Why did the pirate go to school? To improve his arrr‑ticulation.", "Why did the snowman look through the carrots? He was picking his nose.", "Why did the duck get a job? He needed more bills.", "Why did the rope go to therapy? It was at the end of its rope.", "Why did the vacuum break up with the broom? It sucked at relationships.", "Why did the leaf get in trouble? It wouldn’t stop blowing.", "Why did the donut go to school? To get filled with knowledge.", "Why did the cloud get promoted? It had a silver lining.", "Why did the fish join a band? It had great scales.", "Why did the robot go on vacation? It needed to recharge.", "Why did the cookie go to school? It wanted to be a smart cookie.", "Why did the banana call the police? It got split.", "Why did the chair go to therapy? It couldn’t handle the pressure.", "Why did the squirrel bring a suitcase? It was going nuts.", "Why did the toaster break up with the bread? It felt used.", "Why did the moon skip dinner? It was full.", "Why did the spider go to school? To improve its web design.", "Why did the pencil get promoted? It was sharp.", "Why did the blanket get arrested? It covered up too much.", "Why did the cookie sit on the computer? It wanted to be a cookie file.", "Why did the chicken sit at the computer? To search for egg‑samples.", "Why did the astronaut break up with his girlfriend? He needed space.", "Why did the candle stay calm? It always kept its wick together.", "Why did the fish avoid the computer? It was scared of the net.", "Why did the grape get stepped on? It let out a little wine.", "Why did the cow buy a telescope? To see the moooon better.", "Why did the skeleton stay home? He had no body to go with."]  # Gathered using AI
    print(f"\033[32mYay! Good on you, {name}! You came for a laugh!\033[0m")
    print(JOKES[random.randint(0, len(JOKES))])


def random_generator():
    """Do the random utility."""
    random_request = input("Would you like a random N - number or W -word? ").lower()
    if random_request == "n":
        valid = False
        while valid is False:
            try:
                lower_bound = int(input("Enter the lower number: "))
                valid = True
            except ValueError:
                print("\033[31mThat is not valid!\033[0m")
            except TypeError:
                print("\033[31mThat is not valid!\033[0m")
        valid = False
        while valid is False:
            try:
                upper_bound = int(input("Enter the upper number: "))
                if upper_bound <= lower_bound:
                    print("\033[31mThat is not valid!\033[0m")
                else:
                    valid = True
            except ValueError:
                print("\033[31mThat is not valid!\033[0m")
            except TypeError:
                print("\033[31mThat is not valid!\033[0m")
        print(f"Your random number is: {random.randint(lower_bound, upper_bound)}")
    elif random_request == "w":
        valid = False
        words = []
        while valid is False:
            try:
                amount_words = int(input("How many words are you going to add? "))
                if amount_words > 1:
                    valid = True
                else:
                    print("\033[31mThat is not valid!\033[0m")
            except ValueError:
                print("\033[31mThat is not valid!\033[0m")
        for i in range(amount_words):
            words.append(input(f"{i+1}. Enter the word: "))
        print("\n")
        print(words[random.randint(0, amount_words)])
    else:
        print("That is not an option!")


def system_info():
    print("\n###########\nSYSTEM INFO\n###########")
    print(f"Machine: {platform.machine()}")
    print(f"System: {platform.system()}")
    print(f"Platform: {platform.platform()}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")


def utilities():
    """Display other utilities."""
    utility_request = ""
    while utility_request != "b":
        print("\nUtilities: C - Calculator, F - Fun, "
            "R - Random Generators, S - System Info, P - Ping, B - Back to "
            "main menu")
        utility_request = input("Which utility would you"
                                " like to use? ").lower()
        if utility_request == "p":
            ping_utility()
        elif utility_request == "b":
            print("Returning to main menu...")
        elif utility_request == "c":
            calculator()
        elif utility_request == "f":
            fun()
        elif utility_request == "r":
            random_generator()
        elif utility_request == "s":
            system_info()
        else:
            print("\033[31m\nThat is not a valid command. Please enter something else.\033[0m")

"""Actual program starts here."""
if returning == 1:
    welcome_returning(name)
else:
    welcome_first()
    # Reload name after first-time setup
    name = safe_load_json(os.path.join(DATA_DIR, "name.json"), "")

while request != "exit" and request != "quit":
    print("\nFunctions: O - Open an app, Exit - Exit the program, "
          "U - Other Utilities, Help - Help menu")
    request = input("What would you like to do? ").lower()
    if request == "o":
        app_opener()
    elif request == "u":
        utilities()
    elif request == "help":
        print("\nYou asked for help, and I will provide!"
              "I am your computer companion. Tell me a"
              " command, and I will do it. Here "
              "are the commands you can use: "
              "Functions: O - Open an app, Exit - Exit the program, "
              "U - Other Utilities, Help - Help menu\nThanks for using my" \
              " program! I hope you enjoy it! - Charlie")
    elif request == "exit" or request == "quit":
        print("Goodbye!")
    else:
        print("\033[31m\nThat is not a valid command. Please try again.\033[0m")
