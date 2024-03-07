document.addEventListener("DOMContentLoaded", function() 
{
    const searchBar = document.querySelector(".search-bar")
  
    // Event listener for "Enter" key
    searchBar.addEventListener("keydown", function(event) 
    {
      if (event.keyCode === 13) 
      {
        const searchValue = searchBar.value
        const value4url = encodeURIComponent(searchValue.slice(1))
        const domain = window.location.origin
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


  })