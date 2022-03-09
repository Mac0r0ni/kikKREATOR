import logging
import time, sys, json
from kik_unofficial.client impoort KikClient
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

HOST, PORT = "talk11110an.kik.com", 5223
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


def
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

    
        while waiting_for_captcha:
            time.sleep(5)


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
