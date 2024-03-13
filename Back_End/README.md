# **CLOUD COMPUTING PROJECT - Back End**

[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)

---

## Endpoints and Functionalities

### `/signup` (POST)
- **Description**: Manages the Signup page, sending the necessary data to the corresponding page in the Front End. Passwords are hashed to ensure security.
- **Request Body**:
  - `username`: User's username.
  - `password`: User's password.
- **Returns**:
  - `201 OK` if registration is succesful, with user_id as well.
  - `409 Unauthorized` if the user already exists in the database.

### `/login` (POST)
- **Description**: Manages the Login page, sending the necessary data to the corresponding page in the Front End. Passwords are hashed to ensure security.
- **Request Body**:
  - `username`: User's username.
  - `password`: User's password.
- **Returns**:
  - `200 OK` if login is successful, with user_id as well.
  - `401 Unauthorized` if invalid username or password.

### `/alltweets` (GET)
- **Description**: Display all the tweets stored in Redis.
- **Request Body**: None.
- **Returns**: A JSON containing all the tweets.

### `/alltopics` (GET)
- **Description**: Display all the different topics from the tweets stored in Redis.
- **Request Body**: None.
- **Returns**: A JSON containing all the tweets.

### `/tweet` (POST)
- **Description**: Creates a new tweet and stores it in the Redis database.
- **Request Body**:
  - `user`: Username of the user posting the tweet.
  - `content`: Content of the tweet.
  - `topic`: Topic of the tweet.
  - `date`: Date of the tweet.
- **Returns**:
  - `201 Created` if tweet successfully posted.
  - `400 Bad Request` if user not found.

### `/retweet` (POST)
- **Description**: Retweets an existing tweet and stores it in Redis.
- **Request Body**:
  - `tweet_id`: ID of the tweet to retweet.
  - `username`: Username of the user retweeting.
- **Returns**:
  - `201 Created` if retweet successful with new tweet ID.
  - `404 Not Found` if tweet not found.

### `/tweets4topic` (GET)
- **Description**: Retrieves tweets based on a specific topic.
- **Query Parameter**:
  - `topic`: Topic of the tweets to retrieve.
- **Returns**:
  - A JSON array of tweets with the specified topic.
  - `404 Not Found` if no tweets found for the topic.

### `/tweets4user` (GET)
- **Description**: Retrieves tweets posted by a specific user.
- **Query Parameter**:
  - `user`: Username of the user whose tweets to retrieve.
- **Returns**:
  - A JSON array of tweets posted by the specified user.
  - `404 Not Found` if user has no tweets.

---

## Technical Choices and Issues

### CORS Issues :
  
  We had several issues with CORS, whenever we try to fetch data, for Login as well as for research and tweets display. We first used the Flask development environnement as seen during the previous project, but it eventually led us to the following error : 
  
  ```bash
  Access to fetch at 'https://zany-fishstick-jjjjg7964rpcp557-5000.app.github.dev/login' from origin 'https://zany-fishstick-jjjjg7964rpcp557-5501.app.github.dev' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
  ```

  We tried several options, by modifying several parts of the code : 
  * First we used different configurations for the fetch, in *tweets4topic.js* for instance, by trying to turn on or off the *cors mode* ; we also specified explicitly the origin, without any success, and also tried to modify the headers ; we would eventually come back to the initial error.
  * 
  Eventually, we focused on the remaining part of the Back End, with RabbitMQ for instance, which seemed more constructive than solving this issue.

### Codespace and Docker Issues :

  Since the codespace doesn't allow us to work directly with localhost (or 127.0.0.1), we had to modify several parts of the code, notably in the JavaScript files concerning URLs and fetching. Eventually, I tried to use VSCode, but since we don't have admin rights on the school's PCs, I couldn't download Docker; thus, codespace was the best option. Note that the problems occurred only for the binome using codespace; however, the other binome that used their personal PC was able to execute their side of the project, so the tweeting, retweeting, and display of tweets works fine.
