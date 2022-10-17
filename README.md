# mail-socket
To actully send email, we need to rent a mail server. I used Debugging mode to check it ran correctly.

open three powershell
1. Debugging Server
python -m smtpd -n -c DebuggingServer localhost:1025
2. Client.py
HELO kuokuo
MAIL FROM:<mail address>
RCPT TO:<mail address>
DATA
This is a test message.
.
QUIT
3. Server.py
## Reference
Mail content debug mode
https://stackoverflow.com/questions/5619914/sendmail-errno61-connection-refused

multithread structure
http://net-informations.com/python/net/thread.htm
