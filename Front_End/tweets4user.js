function getQuery(value) 
{
    const urlParams = new URLSearchParams(window.location.search)
    return urlParams.get(value)
}

function displayTweet(content, user, topic, date, time)
{
  var container = document.getElementById("tweets_container")
  var title = document.getElementById("title")
  var tweetDiv = document.createElement('div')
  tweetDiv.classList.add('tweet')
  
  var contentDiv = document.createElement('div')
  contentDiv.classList.add('content')
  contentDiv.textContent = content

  var userDiv = document.createElement('div')
  userDiv.classList.add('user')
  userDiv.textContent = user

  var topicDiv = document.createElement('div')
  topicDiv.classList.add('topic')
  topicDiv.textContent = topic

  var dateDiv = document.createElement('div')
  dateDiv.classList.add('date')
  dateDiv.textContent = `${date} ${time}`

  title.textContent = "Tweets of @" + user

  tweetDiv.appendChild(contentDiv)

  tweetDiv.appendChild(userDiv)
  tweetDiv.appendChild(dateDiv)
  tweetDiv.appendChild(topicDiv)
  container.appendChild(tweetDiv)
}

function fetchTweetsFromRedis() {
  let retrieved_tweets = [];
  const user_filter = getQuery("user");

  fetch('http://localhost:5000/tweets4user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ user: user_filter })
  })
  .then(response => response.json())
  .then(tweets => {
    console.log(tweets);
    for (let tweet of tweets) { 
      displayTweet(tweet.content, tweet.user, tweet.topic, tweet.date, tweet.time);
    }
  })
  .catch(error => {
    console.error('Error fetching tweets:', error);
  });
}

document.addEventListener("DOMContentLoaded", function() 
{
  const domain = window.location.origin
  const home = document.getElementById("home")
  const settings = document.getElementById("settings")
  const about = document.getElementById("about")
  home.addEventListener("click", function()
  {
    window.location.href = `${domain}/Front_End/main_page.html`
  })
  settings.addEventListener("click", function()
  {
    window.location.href = `${domain}/Front_End/settings.html`
  })
  about.addEventListener("click", function()
  {
    window.location.href = `${domain}/README.md`
  })

  fetchTweetsFromRedis();
})
