def hello_auth(event, context):
    """Triggered by a change to a Firebase Auth user object.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # The unique id of the user whose auth record changed
    uid = event['uid']
    print(uid)
    print(event)
    email = str(event['email'])
    #email = event['email']
    send_emails(email)
    # print out the uid that caused the function to be triggered
    print(f"Function triggered by change to user: {uid}.")
    # now print out the entire event object
    print(str(event))


def send_emails(email_id):
     import smtplib
     fromaddr = 'desertdevelpomentasu@gmail.com'
     username = 'desertdevelpomentasu'
     password = 'Parker#39'
     server = smtplib.SMTP('smtp.gmail.com', 587)
     server.ehlo()
     server.starttls()
     server.login(username, password)
     to_address = email_id
     #name = i[0]
     email_body = "Welcome to Pitcher. Thank you for signing up!!"
     email_subject = "Welcome from Pitcher"
     message = 'Subject: {}\n\n{}'.format(email_subject, email_body)
     server.sendmail(fromaddr, to_address, message)
     server.quit()