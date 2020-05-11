from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import pyrebase
import nltk
nltk.download('punkt')
nltk.download('stopwords')


 config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": "",
  "serviceAccount": ""
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

  
