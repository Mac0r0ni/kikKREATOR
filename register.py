import logging
import time, sys, json
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError
from kik_unofficial.datatypes.xmpp.login import LoginResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse

from bs4 import BeautifulSoup
from kik_unofficial.datatypes.xmpp.base_elements import  XMPPResponse
from kik_unofficial.datatypes.peers import Group, User
from csv import reader
import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

HOST, PORT = "talk1110an.kik.com", 5223
log = logging.getLogger('kik_unofficial')

captchas = []
global waiting_for_captcha


class KikParsingException(Exception):
    pass

class FetchRosterResponse(XMPPResponse):
    """
    Represents the response to a 'get roster' request which contains the peers list
    """

    def __init__(self, data: BeautifulSoup):
        super().__init__(data)
        self.peers = [self.parse_peer(element) for element in iter(data.query)]
        self.more = data.query.get('more')
        self.timestamp = data.query.get('ts')

    @staticmethod
    def parse_peer(element):
        if element.name == "g":
            return Group(element)
        elif element.name == "item":
            return User(element)
        elif element.name == "remove":
            # deleted accounts / accounts no longer in the roster
            return User(element)
        elif element.name == "remove-group":
            return Group(element)
        else:
            raise KikParsingException("Unsupported peer element tag: {}".format(element.name))


def register(email, username, password, first_name, last_name, birthday="1974-11-20", captcha_result=None):
    """
    Sends a register request to sign up a new user to kik with the given details.
    """

    def main():  # This function is used to execute the login process only if the file was run directly, and not imported.
        RegisterClient()

    class RegisterClient(KikClientCallback):
        def __init__(self):  # Constructor for the SpamBotnet class above
            self.client = KikClient(callback=self, kik_username=None, kik_password=None, device_id_override='IML74K',
                                    android_id_override='dfb2b4172c4eab65')
            log.info("[+] Sending sign up request (name: {} {}, email: {})...".format(first_name, last_name, email))
            print(self.client.register(email, username, password, first_name, last_name, birthday))

        @staticmethod
        def log_format():
            return '[%(asctime)-15s] %(levelname)-6s (thread %(threadName)-10s): %(message)s'

        def on_sign_up_ended(self, response: RegisterResponse):
            global waiting_for_captcha
            waiting_for_captcha = False
            print("\nAccount already exists!!!")
            print("Registered on node {}.".format(response.kik_node))
            print("\n")

        def on_authenticated(self):
            print("Authorized connection initiated.")
            self.client.request_roster()

        def on_login_ended(self, response: LoginResponse):
            print("Logged in as {}.".format(response.username))

        def on_register_error(self, response: SignUpError):
            if "captcha_url" in dir(response):
                print("\nCaptcha URL:", response.captcha_url)

                opt = webdriver.ChromeOptions()
                opt.add_argument("start-maximized")
                #opt.add_argument("--auto-open-devtools-for-tabs")
                mobile_emulation = {"deviceName": "iPhone X"}
                # opt.headless = True
                # opt.add_experimental_option("excludeSwitches", ["enable-logging"])
                opt.add_argument('log-level=3')
                opt.add_experimental_option("mobileEmulation", mobile_emulation)

                # make chrome log requests
                capabilities = DesiredCapabilities.CHROME
                capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs

                driver = webdriver.Chrome('C:\PATH_TO_CHROMEDRIVER.EXE_HERE', desired_capabilities=capabilities, chrome_options=opt)
                driver.get(response.captcha_url)

                print("\n\n----------------------------------------------------------------------------")
                inp = input("Are you done? type anything and press enter once you are done.\n")
                while not inp:
                    time.sleep(2)
                # extract requests from logs
                logs_raw = driver.get_log("performance")
                logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
                driver.close()
                def log_filter(log_):
                    return (
                        # is an actual response
                            log_["method"] == "Network.requestWillBeSent"
                            # and json
                            and "captcha-url?response=" in log_["params"]["documentURL"]
                    )

                reqlist = filter(log_filter, logs)
                result = list(reqlist)[0]["params"]["request"]["url"].split("response=")[1]

                print("Captcha Respnse Fetced...")


                global captchas
                captchas.append([email, username, password, first_name, last_name, birthday, response.captcha_url])

                # result = input("Captcha result:")
                global waiting_for_captcha
                waiting_for_captcha = False

                print("Sending Response to Kik...")
                self.client.register(email, username, password, first_name, last_name, birthday, result)
            else:
                print("Unable to register! error information:\r\n{}".format(response))
                print("Not Waiting")
                waiting_for_captcha = False


        def on_roster_received(self, response: FetchRosterResponse):
            print("Friends: {}".format(response.peers))

    if __name__ == '__main__':  # This is used to execute the login process only if the file was run directly, and not imported.
        # logging.basicConfig(format=RegisterClient.log_format(), level=logging.DEBUG)
        main()

with open('register.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    i = 0

    global header
    for row in csv_reader:
        if not row:
            continue
        i += 1
        if i == 1:
            header = row
            continue

        for j in range(len(row)):
            if not row[j].strip():
                print(header[j], " does not have a valid value on line", i, "in register.csv")

        # row variable is a list that represents a row in csv
        in_email = row[0].strip()
        in_user = row[1].strip()
        in_pass = row[2].strip()
        in_first_name = row[3].strip()
        in_last_name = row[4].strip()
        in_birthday = row[5].strip()

        register(in_email, in_user, in_pass, in_first_name, in_last_name, in_birthday)
        waiting_for_captcha = True

        while waiting_for_captcha:
            time.sleep(5)

print(captchas)
if os.path.exists("credentials.txt"):
    append_write = 'a' # append if already exists
    try:
        with open('credentials.txt', "r+") as f:
            f.seek(0, 2)
            f.seek(f.tell() - 1, 0)
            if f.read() != '\n':
                f.write("\n")
        f.close()
    except:
        pass

else:
    append_write = 'w' # make a new file if not

try:
    with open("credentials.txt", append_write) as a_file:
        for account in captchas:
            us = account[1]
            pa = account[2]
            a_file.write(us + ":" + pa + "\n")
    a_file.close()
except:
    print("Oops! Code ran into an error.")

quit(0)
