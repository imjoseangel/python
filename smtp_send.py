import smtplib
import time
#mynetworks = 168.100.189.0/28, 127.0.0.0/8
From = "sugar@aquanima.com"
Login = From
Password = "sugar"
To = ["josea.munoz@gmail.com"]
Date = time.ctime(time.time())
Subject = "New message from Camille."
Text = "Message Text"

#Format mail message
mMessage = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n%s\n' %
            (From, To, Date, Subject, Text))

print 'Connecting to Server'
server = smtplib.SMTP('180.209.16.210', 465)
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
