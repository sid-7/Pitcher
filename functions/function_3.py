import pyrebase
config = {
  "config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": "",
  "serviceAccount": ""
    }
}
firebase = pyrebase.initialize_app(config)
firebase_storage = firebase.storage()
firebase_auth = firebase.auth()
firebase_database = firebase.database()

def hello_rtdb(event, context):
    data = firebase_database.child("users/investors").get()
    l = []
    for i in data.each():
        v = i.val()
        l.append([v['firstname'], v['email']])
    send_emails(l)
    print("Email sent to investors.")
    
def send_emails(l):
    import smtplib
    fromaddr = 'desertdevelpomentasu@gmail.com'
    username = 'desertdevelpomentasu'
    password = 'Parker#39'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    
    for i in l:
        to_address = i[1]
        name = i[0]
        email_body = "Hello " + name + "A new pitch is available, check it out!!!!"
        email_subject = "New Pitch Avaiable"
        message = 'Subject: {}\n\n{}'.format(email_subject, email_body)
        server.sendmail(fromaddr, to_address, message)
    server.quit()
