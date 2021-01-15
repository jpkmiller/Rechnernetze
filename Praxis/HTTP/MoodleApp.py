import requests
from bs4 import BeautifulSoup
import json
import webbrowser

class MoodleApp:
    cookies = ''

    def __init__(self, username: str = "rnetin", password: str = "ntsmobil"):
        self.m_username = username
        self.m_password = password
        self.login()

    def getsessionid(self):
        r = requests.get('https://moodle.htwg-konstanz.de/moodle/login/index.php')
        soup = BeautifulSoup(r.text, 'html.parser')
        self.cookies = r.cookies
        self.sessionid = soup.find('input', {'name': 'logintoken'})['value']

    def getkeyinfo(self, txt):
        arr = txt.split('\n')
        js = {}
        for s in arr:
            if 'M.cfg' in s:
                ind1 = s.index('{')
                ind2 = s.index('}')
                js = json.loads(s[ind1:ind2 + 1])
                break
        self.sesskey = js['sesskey']
        self.contextid = js['contextid']

    def getuserid(self, txt):
        soup = BeautifulSoup(txt, 'html.parser')
        self.userid = soup.find('div', {'id': 'nav-notification-popover-container'})['data-userid']

    def login(self):
        self.getsessionid()
        payload = {
            'anchor': '',
            'logintoken': self.sessionid,
            'username': str(self.m_username),
            'password': str(self.m_password)
        }
        r = requests.post('https://moodle.htwg-konstanz.de/moodle/login/index.php', data=payload, cookies=self.cookies)

        self.getkeyinfo(r.text)
        self.getuserid(r.text)

    def logout(self):
        url = 'https://moodle.htwg-konstanz.de/moodle/login/logout.php?sesskey=' + self.sesskey
        r = requests.get(url, cookies=self.cookies)

    def downloadTask(self):
        print("downloading task..")
        # TODO: implement method for the download of this lab exercise

        webbrowser.open("https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.docx?forcedownload=1")
        webbrowser.open("https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1")

    def chatLab5(self):
        print("Lab5 chat..")
        # TODO: implement method for receiving and sending messages fom chat "Lab5 Chat"

    def uploadTask(self):
        print("upload task..")
        # TODO: implement method for uploading the submission of this lab exercise

    def test(self):
        print("Test MoodleApp")
        print("Password: " + self.m_password)
        print("Username: " + self.m_username)
        print("SessionID: " + self.sessionid)
        print("SessionKey:  " + self.sesskey)
        print("UserID: " + self.userid)
