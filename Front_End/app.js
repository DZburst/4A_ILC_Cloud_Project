document.addEventListener('DOMContentLoaded', function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (!isLoggedIn) {
        window.location.href = 'login.html';
    }
    // Cache DOM elements
    const loginModal = document.getElementById('loginModal');
    const loginButton = document.getElementById('loginButton');
    const tweetButton = document.getElementById('tweetButton');
    const tweetsContainer = document.getElementById('tweetsContainer');
    const tweetContent = document.getElementById('tweetContent');
    const tweetTopic = document.getElementById('tweetTopic');
    
    // Post tweet event listener
    tweetButton.addEventListener('click', function() {
        const content = tweetContent.value;
        const topic = tweetTopic.value;
        const loggedInUser = localStorage.getItem('username');
        
        const currentDate = new Date();
        const formattedDate = currentDate.toISOString(); 

        fetch('http://localhost:5000/tweet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',  
            credentials: 'include',  // Include credentials in the request
            body: JSON.stringify({ user: loggedInUser, content, topic, date: formattedDate })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            tweetContent.value = ''; // Clear the textarea after posting
            tweetTopic.value = '';   // Clear the topic input after posting
            alert(data.message);
            location.reload(); 
        })
        .catch((error) => {
            console.error('Error:', error); // Log the error details
            location.reload(); 
        });
    });

    function displayTweets() {
        fetch('http://localhost:5000/alltweets')
        .then(response => response.json())
        .then(tweets => {
            const tweetsContainer = document.getElementById('tweetsContainer');
            const tweetTemplate = document.getElementById('tweetTemplate');
    
            tweets.forEach(tweetData => {
                const tweetElement = tweetTemplate.content.cloneNode(true);
    
                tweetElement.querySelector('.text-lg').textContent = tweetData.content;
                tweetElement.querySelector('.text-sm.text-gray-600').textContent = `${tweetData.user} - ${tweetData.topic}`;
                tweetElement.querySelector('.text-sm.text-gray-500').textContent = `${tweetData.date} ${tweetData.time}`;
    
                tweetElement.querySelector('button').addEventListener('click', () => retweet(tweetData.id));
    
                tweetsContainer.appendChild(tweetElement);
            });
        })
        .catch((error) => {
            console.error('Error:', error);
            tweetsContainer.innerHTML = '<p class="text-red-500">Failed to load tweets. Please try again later.</p>';
        });
    }
    

    displayTweets();

    function retweet(tweetId) {
        const loggedInUser = localStorage.getItem('username');
        const retweetData = {
            tweet_id: tweetId,
            username: loggedInUser
        };
    
        fetch('http://localhost:5000/retweet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            credentials: 'include', 
            body: JSON.stringify(retweetData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Retweet failed');
            }
            console.log('Retweet successful');
            location.reload(); 
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    const searchBar = document.getElementById('searchBar');
    const topicsContainer = document.getElementById('topicsContainer'); // Container to display topics

    searchBar.addEventListener('focus', function() {
        fetchTopics();
    });
    function fetchTopics() {
        fetch('http://localhost:5000/alltopics')
            .then(response => response.json())
            .then(data => {
                displayTopics(data.topics);
            })
            .catch(error => console.error('Error fetching topics:', error));
    }
    
    function displayTopics(topics) {
        const topicsContainer = document.getElementById('topicSuggestions');
        if (!topicsContainer) {
            console.error('Topic suggestions container not found');
            return;
        }
    
        // Clear existing topics
        topicsContainer.innerHTML = '';
    
        // Add each topic to the suggestions container
        topics.forEach(topic => {
            const topicDiv = document.createElement('div');
            topicDiv.textContent = topic;
            topicsContainer.appendChild(topicDiv);
    
            // Add event listener for clicking a topic
            topicDiv.addEventListener('click', function() {
                searchBar.value = topic; // Update the search bar with the topic
                // Optionally, you can also automatically trigger a search here
            });
        });
    }
    
    
});
