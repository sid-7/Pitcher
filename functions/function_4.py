from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import pyrebase
import nltk
nltk.download('punkt')
nltk.download('stopwords')

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
firebase_auth = firebase.auth()
firebase_database = firebase.database()


def send_emails(name, email_id):
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
  email_body = "Hello "+ name +"! It seems like the pitch that you just recently uploaded seems similar to the current pitches. Please consider either updating or deleting your pitch. Thank You."
  email_subject = "Regarding your latest pitch"
  message = 'Subject: {}\n\n{}'.format(email_subject, email_body)
  server.sendmail(fromaddr, to_address, message)
  server.quit()


def tokenize(document):
  tokens = word_tokenize(document)
  words = [w.lower() for w in tokens]
  
  porter = nltk.PorterStemmer()
  stemmed_tokens = [porter.stem(t) for t in words]
  
  stop_words = set(stopwords.words('english'))
  filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]
  
  count = nltk.defaultdict(int)
  for word in filtered_tokens:
    count[word] += 1
  return count


def cosine_sim(a,b):
  dot_product = np.dot(a,b)
  norm_a = np.linalg.norm(a)
  norm_b = np.linalg.norm(b)
  return dot_product / (norm_a * norm_b)



def calculateSimilarity(dict1,dict2):
  all_words_list =[]
  
  for key in dict1:
    all_words_list.append(key)
    
  for key in dict2:
    all_words_list.append(key)
  
  all_words_list_size = len(all_words_list)
  
  v1 = np.zeros(all_words_list_size, dtype=np.int)
  v2 = np.zeros(all_words_list_size, dtype=np.int)
  i=0
  
  for (key) in all_words_list:
    v1[i] = dict1.get(key, 0)
    v2[i] = dict2.get(key, 0)
    i+=1

  return cosine_sim(v1,v2)




def hello_rtdb(event, context):  
  resource_string = context.resource
  print(f"Function triggered by change to: {resource_string}.")
  
  data = firebase_database.child("users").child("pitches").get()
  pitches_list = []

  for user in data.each():
    pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
    for pitch in pitches.each():
        pitches_list.append(pitch.val()["description"])
  
  try:
    current_description = list(list(event["delta"].values())[0].values())[0]["description"]
    pitcherId = list(event["delta"].keys())[0]
    pitcher_details = firebase_database.child("users").child("pitchers").child(pitcherId).get()
    email = pitcher_details.val()['email']
    firstname = pitcher_details.val()['firstname']
  except Exception as e:
    print(e)
  
  try:
    curr = tokenize(current_description)
    for description in pitches_list:
      temp = tokenize(description)
      if calculateSimilarity(curr,temp) >= 0.50 and calculateSimilarity(curr,temp) <= 0.95:
        print("Dangerrr!!!!", calculateSimilarity(curr,temp))
        send_emails(firstname,email)
      else:
        print("you are good to go")
      
  except Exception as e:
    print(e)

  