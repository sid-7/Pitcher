# Pitcher

The greatest effect of the internet is the establishment of connections among people around the world. There might be times when a person gets an excited idea about building an innovative product. But the idea does not get implemented as per the plan as the project might need a team of members with different skills. As a result, many ideas are left undeveloped due to lack of financial or technical support. The problems may arise due to unavailability of resources, insufficient contacts to make the idea possible, lack of skills to implement the idea or lack of funds. We try to bridge this gap from idea to implementation by building a web based application named “Pitcher”. “Pitcher” provides a platform for pitchers, contributors and investors to connect over a single project and implement it. A pitcher pitches an idea with a video and description, and the investors and contributors can join the project team. The students and professionals who want to contribute to the projects and expand their skills. Investors can select the project he is interested to fund for. They can select the projects as per their interests and chat with the pitcher and form a team. Thus, Pitcher is a cloud-based web application that connects pitchers, contributors and the investors to a single platform. 

<h1> Architecture </h1>

![Architecture](https://github.com/sid-7/Pitcher/blob/siddharth/Architecture.png)

<h1> Steps to run the application</h1>

- Create a project on Google Cloud Platform with project_id for your choice.
- Create a Google Cloud SQL instance under this project.
- Create a project in Firebase under this project.
- Under the Firebase Authentication, enable the sign-in providers status for Email/Password.
- Create a bucket in Cloud Storage.
- Replace all firebase configurations from the application to your project’s configurations.
- Change the Firebase Realtime database rules as follows.
```
  {
    "rules":{
       ".read":true,
       ".write":true,
    }
  }
 ```		                        

- Change the Firebase Storage rules as follows.

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write;
    }
  }
}
```                  
		
- Download the  Google Cloud SDK.

- Create a Cloud Function from the gcloud console with the following parameters.
```
Name: <you_choice>
Memory_allocated: 128MiB
Trigger: Firebase Authentication
Event-Type: Create
Runtime: Python
Copy the contents of functions/function1.py into the code panel.
```
- Create a Cloud Function from the gcloud console with the following parameters.
```
Name: <you_choice>
Memory_allocated: 128MiB
Trigger: Firebase Authentication
Event-Type: Delete
Runtime: Python
Copy the contents of functions/function2.py into the code panel.
```
- Create a Cloud Function from the gcloud console with the following parameters.
```
Name: <you_choice>
Memory_allocated: 256MiB
Trigger: Firebase Realtime Database
Event_Type: Write
Database: <Your_realtime_database_name>
Path: user/pitches
Runtime: Python
Copy the contents of functions/function3.py into the code panel.
```
- Create a Cloud Function from the gcloud console with the following parameters.
```
Name: <you_choice>
Memory_allocated: 256MiB
Trigger: Firebase Realtime Database
Event_Type: Write
Database: <Your_realtime_database_name>
Path: user/pitches
Runtime: Python
Copy the contents of functions/function4.py into the code panel.
```
- Install  Python 3.7 and libraries mentioned in requirements.txt.
```$:~  pip install requirements.txt```

- Copy the contents of the /application/ to a folder of your choice.
- Download the Google Cloud SQL proxy for migrating the local django database.
- Run the following code in Google Cloud SDK Shell and fetch the Connection_Name:
```$:~  gcloud sql instance describe [YOUR_INSTANCE_NAME]```

- Initialize the Google Cloud Proxy using the Connection_Name as follows:

```cloud_sql_proxy.exe-instances="[YOUR_INSTANCE_CONNECTION_NAME]"=tcp:5432```

- Change the settings.py in the application folder and replace the DATABASES section as below:
		

- Run the following commands to migrate the django database to the Cloud SQL Instance.
```
    application\$:~ python manage.py makemigrations
    application\$:~ python manage.py makemigrations [application_name]
    application\$:~ python manage.py migrate
```

- Collect the static content of the application using the below command.
	  ```  	    application\$:~ python manage.py collectstatic```

- Set the cloud storage bucket read operation as public.
			```$:~ gsutil defacl set public-read gs://<your-gcs-bucket>```

- Uploading the static content to the bucket. Write the below line in google cloud SDK command line.
	```		application\$:~ gsutil rsync -R static/ gs://<your-gcs-bucket>/static```

- Change the STATIC_URL in settings.py in the application folder to the following:
	```		http://storage.googleapis.com/<your-gcs-bucket>/static```

- Deploy the application.
	```		application\$:~ gcloud app deploy```

- Open the Application URL
	```		application\$:~ gcloud app browse ```
