// Fetch the menu.html file
fetch('/templates/menu.html')
  .then(function(response) {
    return response.text();
  })
  .then(function(data) {
    // Insert the menu.html content into the 'menu' div
    document.getElementById('menu').innerHTML = data;

    // Add event listener to the 'Writer' button
    var writerButton = document.getElementById('writer-button');
    writerButton.addEventListener('click', function() {
      // Open the desired page when the button is clicked
      window.location.href = '/templates/writer.html';
    });

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

  })
  .catch(function(error) {
    console.error('Error:', error);
  });
