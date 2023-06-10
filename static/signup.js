document.getElementById("signup-form").addEventListener("submit", function(event) {
  event.preventDefault();

  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var email = document.getElementById("email").value;
  var fname = document.getElementById("fname").value;
  var lname = document.getElementById("lname").value;
  var data = {
    "username": username,
    "password": password,
    "email": email,
    "fname": fname,
    "lname": lname
  };

  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
      if (result.success) {
        window.location.href = "login.html";
      } else {
        alert("Error: " + result.message);
      }
    })
  .catch(error => {
      console.error("Error:", error);
    });
});
