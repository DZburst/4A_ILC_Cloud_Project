document.addEventListener("DOMContentLoaded", function() 
{
  const searchBar = document.querySelector(".search-bar")
  const domain = window.location.origin

  // Event listener for "Enter" key
  searchBar.addEventListener("keydown", function(event) 
  {
    if (event.keyCode === 13) 
    {
      const searchValue = searchBar.value
      const value4url = encodeURIComponent(searchValue.slice(1))
      if (searchValue[0] === "#")
      {
        const searchResultsUrl = `${domain}/tweets4topic?topic=${value4url}`
        // const searchResultsUrl = `${domain}/Front_End/tweets4topic.html}`
        window.location.href = searchResultsUrl
      }
      else if (searchValue[0] === "@")
      {
        const searchResultsUrl = `${domain}/tweets4user?user=${value4url}`
        // const searchResultsUrl = `${domain}/Front_End/tweets4user.html}`
        window.location.href = searchResultsUrl
      }
      else
      {
        alert("Please type in a valid topic or username. \nA username should start with @, and a topic with #.")
      }
    }
  })

  const top_topics = document.getElementById("top_topics")

  top_topics.addEventListener('click', function(event) 
  {
    if (event.target.tagName === 'LI') 
    {
      var topic = event.target.innerText
      const value4url = encodeURIComponent(topic.slice(1))
      const searchResultsUrl = `${domain}/Front_End/tweets4topic.html?topic=${value4url}`
      window.location.href = searchResultsUrl
    }
  })
})