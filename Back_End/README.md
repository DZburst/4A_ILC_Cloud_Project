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

## Technical Choices / Issues

### CORS Issues : `SOLVED`
  
  After several attempts, we were able to find the cause of the fetch issues thrown by CORS : some requests were set to GET rather than POST in the JS files, plus some paths weren't correct, because of the problem with Codespace.

### Codespace and Docker Issues : `NO MORE RELEVANT`

  Since the codespace doesn't allow us to work directly with localhost (or 127.0.0.1), we had to modify several parts of the code, notably in the JavaScript files concerning URLs and fetching. Eventually, I tried to use VSCode, but since we don't have admin rights on the school's PCs, I couldn't download Docker; thus, codespace was the best option. Note that the problems occurred only for the binome using codespace; however, the other binome that used their personal PC was able to execute their side of the project, so the tweeting, retweeting, and display of tweets works fine.
