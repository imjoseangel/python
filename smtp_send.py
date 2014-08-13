import smtplib
import time
#mynetworks = 168.100.189.0/28, 127.0.0.0/8
From = "<from_address>"
Login = From
Password = "<your_password>"
To = ["<destination_email>"]
Date = time.ctime(time.time())
Subject = "New message"
Text = "Message Text"

#Format mail message
mMessage = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n%s\n' %
            (From, To, Date, Subject, Text))

print 'Connecting to Server'
server = smtplib.SMTP('<your_ip>', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(Login, Password)

#Send mail
rCode = server.sendmail(From, To, mMessage)
server.quit()

if rCode:
    print 'Error Sending Message'
else:
    print 'Message Sent Successfully'
