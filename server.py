import socket
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sender_replace_word_dictionary = {"MAIL FROM:<": "", ">": ""}
receiver_replace_word_dictionary = {"RCPT TO:<": "", ">": ""}


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)

    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def run(self):
        print("Connection from : ", clientAddress)
        self.csocket.send(bytes("Hi, This is from Server.", 'utf-8'))
        msg = ''
        mail_text = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if "MAIL FROM:" in msg:
                sender_address = ClientThread.replace_all(
                    msg, sender_replace_word_dictionary)
            elif"RCPT TO:" in msg:
                receiver_address = ClientThread.replace_all(
                    msg, receiver_replace_word_dictionary)
            elif msg == 'QUIT':
                break
            else:
                mail_text = mail_text + msg
            print("From Client : ", msg)

            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Client at ", clientAddress, " disconnected...")

        # SMTP
        mail_content = MIMEMultipart()
        mail_content["subject"] = "KUO-MAIL-SERVER TESTING"
        mail_content["from"] = sender_address
        mail_content["to"] = receiver_address
        # mail_content.attach(MIMEText(mail_text))

        s = smtplib.SMTP('localhost', 1025)
        s.sendmail(mail_content["from"], mail_content["to"], mail_text)
        s.quit()


LOCALHOST = "127.0.0.2"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request.")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
