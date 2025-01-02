# STEPS TO RUN IN WINDOWS TERMINAL
### 0. Install the packages in requirements.txt. 
### 1. Used railway postgres for hosting the database
### 2. Used railway redis server for broker database for celery  
### 3. Created tests and jwt authentication
### 4. Reports are in reports directory
### 5. Domain - https://library-production-a0cd.up.railway.app/
### 6. Authentication steps: 
#### 1. Send a post request to https://library-production-a0cd.up.railway.app/token  with Usernamw = messileo  Password = messileo@18122022
#### 2. Now add a key value pair to http requests with key = Authorization   Value = Bearer generated_access_token
