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


function getQuery(value) 
{
    const urlParams = new URLSearchParams(window.location.search)
    return urlParams.get(value)
}


function fetchTweetsFromRedis() 
{
  // AJAX request to the API
  let retrieved_tweets = []
  const topic_filter = getQuery("topic")
  const value4url = encodeURIComponent(topic_filter)
  fetch(`http://127.0.0.1:5000/tweets4user?user=${value4url}`,
  {
    method: 'GET',
    mode: 'cors',
    headers : {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(tweets => 
    {
      console.log(tweets)
      for (let i = 0; i < tweets.length; i++) 
      {
        let tweet = tweets[i]
        retrieved_tweets.push(tweet)
      }
      for (let tweet_value in retrieved_tweets)
      {
        let content = tweet_value["content"]
        let user = tweet_value["user"]
        let topic = tweet_value["topic"]
        let date = tweet_value["date"]
        let time = tweet_value["time"]
        displayTweet(content, date, time, topic, user)
      }
    })
    .catch(error => {
      console.error('Error fetching tweets:', error)
    })
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