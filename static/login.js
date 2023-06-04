function login() {
  event.preventDefault();

  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  // Send the username and password to the server for authentication
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/login", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // Handle the server response
      var response = JSON.parse(xhr.responseText);
      if (response.success) {
        window.location.href = "src.html";
      } else {
        alert("Error: " + response.message);
      }
    }
  };

  // Convert user data to a URL-encoded string
  var data = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password);

  // Send the AJAX request
  xhr.send(data);
}
