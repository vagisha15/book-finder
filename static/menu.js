// Fetch the menu.html file
fetch('/templates/menu.html')
  .then(function(response) {
    return response.text();
  })
  .then(function(data) {
    // Insert the menu.html content into the 'menu' div
    document.getElementById('menu').innerHTML = data;

    // Get the username from the Flask application
    fetch('/get_username')
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        var username = data.username;

        // Add event listener to the 'Writer' button
        var writerButton = document.getElementById('writer-button');
        writerButton.addEventListener('click', function() {
          // Check if the username is not empty
          if (username !== "") {
            // Open the desired page when the button is clicked
            window.location.href = '/templates/writer.html';
          } else {
            // Display a message asking the user to login first
            alert('Please login first');
          }
        });

        // Rest of the code...

        var homeButton = document.getElementById('reader-button');
        homeButton.addEventListener('click', function() {
          // Open the desired page when the button is clicked
          window.location.href = '/';
        });

        var loginButton = document.getElementById('login-button');
        loginButton.addEventListener('click', function() {
          // Open the desired page when the button is clicked
          window.location.href = '/templates/login.html';
        });

        var signupButton = document.getElementById('signup-button');
        signupButton.addEventListener('click', function() {
          // Open the desired page when the button is clicked
          window.location.href = '/templates/signup.html';
        });

        var logo = document.getElementById('logo');
        logo.addEventListener('click', function() {
          // Open the desired page when the button is clicked
          window.location.href = '/';
        });

        var aboutButton = document.getElementById('contact-button');
        aboutButton.addEventListener('click', function() {
          // Open the desired page when the button is clicked
          window.location.href = '/templates/about.html';
        });

      })
      .catch(function(error) {
        console.error('Error:', error);
      });
  })
  .catch(function(error) {
    console.error('Error:', error);
  });
