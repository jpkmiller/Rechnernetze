import socket, time, datetime, base64

AUTH = "AUTH LOGIN"
LOGIN = "rnetin"
PASSWORD = "ntsmobil"
MAIL_SERVER = "asmtp.htwg-konstanz.de"
PORT = 587
NEW_LINE = "\r\n"


def main():
    print("Convert Login (" + LOGIN + ") and Password (" + PASSWORD + ") to Base64-Code...")
    loginBase64 = (base64.b64encode(LOGIN.encode('utf-8'))).decode('utf-8')
    passwordBase64 = (base64.b64encode(PASSWORD.encode('utf-8'))).decode('utf-8')
    print("Converted Login: " + loginBase64)
    print("Converted Password: " + passwordBase64 + "\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.setblocking(True)

    print("Connecting to HOST with mail server " + MAIL_SERVER + " on port " + str(PORT) + "...")
    sock.connect((MAIL_SERVER, PORT))

    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("Start Login with command" + AUTH + "...")
    command = (AUTH + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("Send Login Username in Base64-Code for Authentication...")
    command = (loginBase64 + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("Send Password in Base64-Code for Authentication...")
    command = (passwordBase64 + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("Get data from user...")
    senderAddress = input("Please enter email address of sender: ")
    receiverAddress = input("Please enter email address of receiver: ")
    subject = input("Please enter a subject: ")
    text = input("Please enter a message text: ")

    print("\nGive address of sender with command: MAIL FROM:  <" + senderAddress + "> ...")
    command = ("MAIL FROM: <" + senderAddress + ">" + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("\nGive address of receiver with command: RCPT TO:  <" + receiverAddress + "> ...")
    command = ("RCPT TO: <" + receiverAddress + ">" + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("Command: DATA ...")
    command = ("DATA" + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    print("\nSend subject and text with command: Subject: " + subject + "\n" + text)
    command = ("Subject: " + subject + "\n" + text + "\n." + NEW_LINE)
    sock.send(command.encode('utf-8'))
    responseMsg = sock.recv(1024).decode('utf-8')
    print("Response message: " + responseMsg + "\n")

    sock.close()
    print("Socket closed")


main()
