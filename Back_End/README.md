# **CLOUD COMPUTING PROJECT - Back End**

[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)

---

## **Endpoints and functionnalities**

* <u>**/alltweets**</u>

  Simply display all the tweets stored in Redis.

* <u>**/login**</u>

  Manages the Login page, to send the necessary data to the corresponding page in the Front End. Also, the passwords are hashed to guaranty the security, and a message is sent for the alert in the front depending on the credentials.

* <u>**/tweet**</u>

  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut varius posuere leo, a egestas tellus eleifend sed. Vestibulum egestas fermentum dolor vel sodales. Fusce vitae tortor lacinia, interdum quam vitae, dictum eros. Fusce non fringilla nunc. Cras et sapien metus. Proin semper pretium orci in hendrerit. Ut nec turpis tincidunt, vehicula turpis nec, sagittis tortor. Cras nec posuere enim. Vivamus felis neque, rhoncus quis dui id, porta molestie nulla.

* <u>**/retweet**</u>

  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut varius posuere leo, a egestas tellus eleifend sed. Vestibulum egestas fermentum dolor vel sodales. Fusce vitae tortor lacinia, interdum quam vitae, dictum eros. Fusce non fringilla nunc. Cras et sapien metus. Proin semper pretium orci in hendrerit. Ut nec turpis tincidunt, vehicula turpis nec, sagittis tortor. Cras nec posuere enim. Vivamus felis neque, rhoncus quis dui id, porta molestie nulla.

* <u>**/tweets4topic**</u>

  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut varius posuere leo, a egestas tellus eleifend sed. Vestibulum egestas fermentum dolor vel sodales. Fusce vitae tortor lacinia, interdum quam vitae, dictum eros. Fusce non fringilla nunc. Cras et sapien metus. Proin semper pretium orci in hendrerit. Ut nec turpis tincidunt, vehicula turpis nec, sagittis tortor. Cras nec posuere enim. Vivamus felis neque, rhoncus quis dui id, porta molestie nulla.

* <u>**/tweets4user**</u>

  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut varius posuere leo, a egestas tellus eleifend sed. Vestibulum egestas fermentum dolor vel sodales. Fusce vitae tortor lacinia, interdum quam vitae, dictum eros. Fusce non fringilla nunc. Cras et sapien metus. Proin semper pretium orci in hendrerit. Ut nec turpis tincidunt, vehicula turpis nec, sagittis tortor. Cras nec posuere enim. Vivamus felis neque, rhoncus quis dui id, porta molestie nulla.


## **Technical choices and Issues**

* <u>**Problem between the Codespace and CORS**</u>
  
  We've had several issues with CORS, whenever we try to fetch data, for Login as well as for research and tweets display. We first used the Flask development environnement as seen during the previous project, but it eventually led us to the following error : 
  
  ```bash
  Access to fetch at 'https://zany-fishstick-jjjjg7964rpcp557-5000.app.github.dev/login' from origin 'https://zany-fishstick-jjjjg7964rpcp557-5501.app.github.dev' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
  ```

  We tried several options, by modifying several parts of the code : 
  * First we used different configurations for the fetch, in *tweets4topic.js* for instance, by trying to turn on or off the *cors mode* ; we also specified explicitly the origin, without any success, and also tried to modify the headers ; we would eventually come back to the initial error.
  * Then we also modified the code of the API, notably in the endpoints concerned and the instanciation of the Redis database, as well as the CORS instanciation. We added the *cross-origin* operator below the route, we tried specifying explicitly the origin and port as well, and used the IP *172.17.0.2* ; none of these worked...