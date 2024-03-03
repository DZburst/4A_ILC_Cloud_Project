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
    

    // Login event listener
    loginButton.addEventListener('click', function() {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
        })
        .catch((error) => {
            alert(error.message);
        });
        isLoggedIn = true;
        loginModal.style.display = 'none'; 
    });

    // Post tweet event listener
    tweetButton.addEventListener('click', function() {
        const content = tweetContent.value;
        const topic = tweetTopic.value;
        const loggedInUser = localStorage.getItem('username');
        fetch('http://localhost:5000/tweet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: loggedInUser, content, topic }) // Use the logged-in username
        })
        .then(response => response.json())
        .then(data => {
            tweetContent.value = ''; // Clear the textarea after posting
            tweetTopic.value = '';   // Clear the topic input after posting
            alert(data.message);
            displayTweets(); 
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Function to fetch and display all tweets
    function displayTweets() {
        fetch('http://localhost:5000/alltweets')
        .then(response => response.json())
        .then(tweets => {
            tweetsContainer.innerHTML = tweets.map(tweet => `
                <div class="max-w-md mx-auto bg-white rounded-lg overflow-hidden md:max-w-lg my-2">
                    <div class="md:flex">
                        <div class="w-full p-4">
                            <p>${tweet.content}</p>
                            <div class="text-sm text-gray-600">${tweet.user} - ${tweet.topic}</div>
                            <div class="text-sm text-gray-500">${tweet.date} ${tweet.time}</div>
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    displayTweets();
});
