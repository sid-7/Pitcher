# import pyrebase
# import firebase_admin
# from firebase_admin import credentials, firestore, storage
#
#
#
#
# config = {
#   "apiKey": "AIzaSyBTlSwWe6lD6NLi8OrDPe49qWIllNgttMI",
#   "authDomain": "pitcher-275100.firebaseapp.com",
#   "databaseURL": "https://pitcher-275100.firebaseio.com",
#   "storageBucket": "pitcher-275100.appspot.com",
#   "serviceAccount": "serviceAccountCredentials.json"
# }
#
# cred=credentials.Certificate('serviceAccountCredentials.json')
#
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'pitcher-275100.appspot.com'
# })
# db = firestore.client()
# bucket = storage.bucket()
#
# firebase = pyrebase.initialize_app(config)
#
# firebase_auth = firebase.auth()
# firebase_database = firebase.database()
