import pyrebase
config = {
  "apiKey": "AIzaSyBTlSwWe6lD6NLi8OrDPe49qWIllNgttMI",
  "authDomain": "pitcher-275100.firebaseapp.com",
  "databaseURL": "https://pitcher-275100.firebaseio.com",
  "storageBucket": "pitcher-275100.appspot.com",
  "serviceAccount": {
      "type": "service_account",
      "project_id": "pitcher-275100",
      "private_key_id": "175f7a5d189fd31eee16dea3831a826ac3b547f9",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0CqzcbMce3Q/i\ng8IZ/QcbcM2r40Oqn7McD9T67OueOKMIzKzSawitxTmB3/q6Exj4O1q41nmH9YgW\nxgw68mDfWkKJr9l9c1jGDbVJeWbOYSkyG2Kh8dV0kOeOeHivqOirSKkiWlTnFed4\natnePaqbg6cND/0Dgwl7JRFvDAtqsg2xL4Rca0EuVRuSksQK542W6MSiOi6ulELj\nWFNuEceXDsmEyGpW1N+h8kexrVO6zI95Y6Fanc2P3rs4Cu8SjwZZkWlR2pWS4mP4\nfjfJ9GM+lSpLzYbnJF7hK68uGrITPww1tw6jN4Kjte/mmsurU1MxjcG71IBSOSVt\nJ9NIHM4hAgMBAAECggEAAXqRd9LaZ1aI5/3C+UBBanr963lM79tgMZ0FLTBHO/1V\nLyWG5AhjnGbGwu+eUUsxHNqC83VKhKtSUZ/mj5DjAA6kxi6oM7OKoVTRPiq1usCk\nTEWv5OqLNpSunDZWhRiBxw9hmUHtRC54lbNTTwlKC+fey5i2ewIHZh1/CUlrv2sh\nAMG1U4UiZQj9i2Jb5PrCWo1wAFimkd7qm++F8vh6tg9u5ECbHW5r/k17VUjHK2FA\nnYA6LMSRHV7iuDtjKe91EhH0TYgjWuQpce3ilhJf9WHSIOLWr6qpmE7RRj/3VymD\nBh94UhkDbKIPDWHdPhiCQdiGDuWc8GzVn7euqU4/oQKBgQDzy64Z4hRmmJTjf157\nPMXts6OkeHF/pvKqJ+nSQjyqPBkpIsL/43LYuCYW7U9hJv2fd3Zv9Bx2q/3oQw4e\ns1mxj3Cfvihm8BnQIdxoxEjf8dDPe164aYH+1xP6oayP/yT3VX705lDN09uY72Rs\n299n3Qq+knWNRDT7xjuMpa17UQKBgQC9DffLqixozSu4rfjDlM98+5B6r3fV6wEE\n5cZDljKtdOOd9NZgdzWs7BGFUDansp6RzUB5bt8VkUQeGhdbca2we+IwuYNFyVtU\n62ua7VrPAzyNXWr8xyS81LsRJ8Av2VG8HcomWSDf+vXQuNUYQ/L3+3b9fg+0cEV9\n52B0N27R0QKBgCx6y8/zHI+/ZOLA2UcYxm/g54lZZDPLDNkYoSN4bEMO5fRIYFV5\ndPmvV1u1flcWWw2eKSCx5AOOy6t1mHzncgTgS8cJVau6QKtlkiYXMciSAOvp8VUq\nAsqxCPcgSjCXd3IcyiX6Y2G6NoWHn8Xws6jqfkxYwlO8zwHkn/bAP4+RAoGAQbXo\nKg8FDow5pSA69ef0UnGx3yK8GUtseEJRLk63YJjfQJjIJpFow6jt0hN2W8V23iCk\nR1DlEz8BmSDie3NAtrXogZ0JZqk9KIAHT7suNAPg+RW+SQwC1etu9eCGKVt00Fje\nWYPjLFazOA/2aU+81Lq/ug4l8UaQsNlKKjrWNvECgYEAo3Srh9mQtHE/Qnnurpyx\n9MSNZjmIycXEU7O7QM+d/Gr+cv/4DMEZ4yNde+NsW53GJp4uvFBXmWi1k6v5wLVA\nYDv8iGuqwu9OVKAA+1/eAkAvbr/Ew34RpCQ911tyryUA6YsGx5ilgN2wVfcoqbOi\nlGvnLBV8avJQDJgrOsHhQok=\n-----END PRIVATE KEY-----\n",
      "client_email": "firebase-adminsdk-dodyf@pitcher-275100.iam.gserviceaccount.com",
      "client_id": "115985643563375262745",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dodyf%40pitcher-275100.iam.gserviceaccount.com"
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