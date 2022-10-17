import socket


SERVER = "127.0.0.2"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
# client.sendall(bytes("This is from Client", 'UTF-8'))
print("220 KUO-MAIL-SERVER. Only Uppercase Is Available.")
while True:
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())
    while True:
        out_data = input()
        if "HELO" in out_data:
            name = out_data[5:]
            print("250 HELLO", name)
            break
        else:
            print("503 5.5.1 Error: send HELO first")
    while True:
        out_data = input()
        if "MAIL FROM:<" and ">" in out_data:
            # print("sender mail address: ", sender_address)
            if "@" not in out_data:
                print("sender address is not completeness")
            else:
                client.sendall(bytes(out_data, 'UTF-8'))
                print("250 2.1.0 Ok")
                break
        else:
            print("501 5.5.4 Syntax: MAIL FROM:<address>")
    while True:
        out_data = input()
        if "RCPT TO:<" and ">" in out_data:
            if "@" not in out_data:
                print("receiver address is not completeness")
            else:
                client.sendall(bytes(out_data, 'UTF-8'))
                print("250 2.1.0 Ok")
                break
        else:
            print("501 5.5.4 Syntax: RCPT TO:<address>")

    mail_content = ""
    while True:
        out_data = input()
        if "DATA" == out_data:
            print("354 Enter mail, end with . on a line by itself")
            while True:
                out_data = input()
                if "." == out_data.replace("\n|\t", ""):
                    print("End of DATA state.")
                    break
                else:
                    mail_content = mail_content + out_data + '\n'
            client.sendall(bytes(mail_content, 'UTF-8'))
            break
        else:
            print("501 5.5.4 Syntax: DATA")

    while True:
        out_data = input()
        if "QUIT" == out_data:
            print("221 KUO-MAIL-SERVER closing connection")
            client.sendall(bytes("QUIT", 'UTF-8'))
            break
        else:
            print("501 5.5.4 Syntax: QUIT")
    break
client.close()
