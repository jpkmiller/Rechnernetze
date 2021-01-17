import os
import re
import time
import numpy as np

import requests
from bs4 import BeautifulSoup
import json
import webbrowser


class MoodleApp:

    def __init__(self, username: str = "rnetin", password: str = "ntsmobil"):
        self.session = requests.Session()  # session for cookies, etc.

        self.m_username = username
        self.m_password = password
        self.login_token = ''
        self.session_key = ''  # session key provided by moodle
        self.context_id = 0  # moodle needs this to know in which context its in
        self.user_id = 0
        self.response = ''
        self.login()

    def get_logintoken(self):
        r = self.session.get('https://moodle.htwg-konstanz.de/moodle/login/index.php')
        soup = BeautifulSoup(r.text, 'html.parser')
        self.login_token = soup.find('input', {'name': 'logintoken'})['value']

    def get_key_info(self, txt, typ=None):
        arr = txt.split('\n')
        js = {}
        for s in arr:
            if 'M.cfg' in s:
                ind1 = s.index('{')
                ind2 = s.index('}')
                js = json.loads(s[ind1:ind2 + 1])
                break

        if typ is not None:
            if typ == 'session_key':
                return js['sesskey']
            elif typ == 'context_id':
                return js['contextid']

        self.session_key = js['sesskey']
        self.context_id = js['contextid']

    def get_user_id(self, txt):
        soup = BeautifulSoup(txt, 'html.parser')
        self.user_id = soup.find('div', {'id': 'nav-notification-popover-container'})['data-userid']

    def login(self):
        self.get_logintoken()
        payload = {
            'anchor': '',
            'logintoken': self.login_token,
            'username': self.m_username,
            'password': self.m_password
        }
        r = self.session.post('https://moodle.htwg-konstanz.de/moodle/login/index.php', data=payload,
                              cookies=self.session.cookies)
        self.response = r.text
        self.get_key_info(r.text)
        self.get_user_id(r.text)

    def logout(self):
        url = 'https://moodle.htwg-konstanz.de/moodle/login/logout.php?sesskey=' + self.session_key
        r = self.session.get(url, cookies=self.cookies)

    def download_task(self):
        print("downloading task..")
        # TODO: implement method for the download of this lab exercise

        # webbrowser.open("https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.docx?forcedownload=1")
        # webbrowser.open("https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1")

        # r = self.session.get('https://moodle.htwg-konstanz.de/moodle/pluginfile.php')
        # self.cookies = r.cookies

        r = self.session.get(
            'https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf',
            cookies=self.cookies, stream=True)
        with open('Praxis/HTTP/DownloadContent/task.pdf', 'wb') as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                pdf.write(chunk)

    def fetch_notifications(self):
        def get_context_id(session):
            r = session.get('https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183',
                            cookies=session.cookies)
            return self.get_key_info(r.text, 'context_id')

        JSON = [
            {
                "index": 0,
                "methodname": "core_fetch_notifications",
                "args": {
                    "contextid": get_context_id(self.session)
                }
            }
        ]
        payload = json.dumps(JSON)
        messages = self.session.post(
            'https://moodle.htwg-konstanz.de/moodle/lib/ajax/service.php?sesskey=' + self.session_key + '&info=core_fetch_notifications',
            data=payload,
            cookies=self.session.cookies
        )

    def receive_message(self):
        def get_messages_from_response(response):
            # TODO: BeautifulSoup does not work as expected here
            soup = BeautifulSoup(response, 'html.parser')
            author = soup.find('tr').find('th', {'class': 'title'})
            content = soup.find('tr').find('td', {'class': 'text'})
            print(content)
            print(author)
            return np.asarray(author, content).T

        last = round(time.time())
        JSON = {
            "message": "",
            "id": "183",
            "groupid": "0",
            "last": last,
            "sesskey": self.session_key,
            "refresh": "Aktualisieren"
        }

        r = self.session.post('https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183',
                              data=JSON,
                              cookies=self.session.cookies)
        """
        r = self.session.get(
             'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183',
           cookies=self.session.cookies
        )
        """
        print(r.text)
        print(get_messages_from_response(r.text))

    def chat(self, message: str):
        last = round(time.time())
        JSON = {
            "message": message,
            "id": "183",
            "groupid": "0",
            "last": last,
            "sesskey": self.session_key
        }
        # JSON must not be dumped!!
        # It must have application/x-www-form-urlencoded format to which it is automatically converted
        self.session.post('https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183',
                          data=JSON,
                          cookies=self.session.cookies)
        self.receive_message()

    def upload_task(self):
        print("upload task..")
        # TODO: implement method for uploading the submission of this lab exercise

    def tui(self):
        while True:
            i = input("Chat / Info / Download / Upload / Exit\n")
            if i == "Chat" or i == "chat":
                while True:
                    i = input("Message: ")
                    if i == "Exit" or i == "exit":
                        break
                    self.chat(i)
                continue
            elif i == "Info" or i == "info":
                self.get_infos()
            elif i == "Download" or i == "download":
                self.download_task()
            elif i == "Upload" or i == "upload":
                self.upload_task()
            elif i == "Exit" or i == "exit":
                exit(0)

    def get_infos(self):
        print("Test MoodleApp")
        print("Password: " + self.m_password)
        print("Username: " + self.m_username)
        print("SessionID: " + self.login_token)
        print("SessionKey:  " + self.session_key)
        print("UserID: " + str(self.user_id))


if __name__ == '__main__':
    moodleApp = MoodleApp()
    moodleApp.tui()
