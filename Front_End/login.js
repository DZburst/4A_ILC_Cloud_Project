document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const username = usernameInput.value;
        const password = passwordInput.value;

        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('username', username);
            window.location.href = 'main_page.html'; 
        })
        .catch(error => {
            alert(error.message);
        });
    });
    // Sign-up modal functionality
    const signupBtn = document.getElementById('signup-btn');
    const signupModal = document.getElementById('signup-modal');
    const closeBtn = document.querySelector('.close');

    // Show the signup modal
    signupBtn.addEventListener('click', function() {
        signupModal.style.display = 'block';
    });

    // Close the signup modal
    closeBtn.addEventListener('click', function() {
        signupModal.style.display = 'none';
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        if (event.target === signupModal) {
            signupModal.style.display = 'none';
        }
    });

    // Handle the sign-up form submission
    const signupForm = document.getElementById('signup-form');
    const newUsernameInput = document.getElementById('new-username');
    const newPasswordInput = document.getElementById('new-password');

    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const username = newUsernameInput.value;
        const password = newPasswordInput.value;

        fetch('http://localhost:5000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Sign-up failed');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            // Optionally clear the form or close the modal
            signupModal.style.display = 'none';
        })
        .catch(error => {
            alert(error.message);
        });
    });
});
