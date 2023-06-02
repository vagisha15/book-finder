document.getElementById("myForm").addEventListener("submit", function(event) {
  event.preventDefault();
  document.getElementById("header").style.display = "none";
  document.getElementById("inputDiv").style.display = "none";
  var inputString = document.getElementById("inputString").value;
  var url = "/api/images";
  var requestData = { inputString: inputString };
  console.log(requestData);
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    // Process the response data
    console.log(data);
    displayImages(data.imageUrls, data.titles, data.authors, data.types, data.genres);
  })
  .catch(function(error) {
    console.error("Error:", error);
  });
});

document.getElementById("green-panel").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submission
  var inputString = document.getElementById("inputString").value;
  var url = "/api/images";
  var requestData = { inputString: inputString };
  console.log(requestData);
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    // Process the response data
    console.log(data);
    displayImages(data.imageUrls, data.titles, data.authors, data.types, data.genres);
  })
  .catch(function(error) {
    console.error("Error:", error);
  });
});

// Create the submit button for the green-panel
var submitButton = document.createElement("button");
submitButton.textContent = "Submit";
document.getElementById("green-panel").appendChild(submitButton);

var clearButton = document.createElement("button");
clearButton.textContent = "Clear Filters";
document.getElementById("green-panel").appendChild(clearButton);

submitButton.addEventListener("click", function(event) {
  event.preventDefault(); // Prevent form submission
  var inputString = document.getElementById("inputString").value;
  var url = "/api/images";
  var typeDropdown = document.getElementById("type-dropdown").value;
  var genreDropdown = document.getElementById("genre-dropdown").value;
  var authorDropdown = document.getElementById("author-dropdown").value;
  var requestData = { inputString: inputString ,filterValue: "book_author-"+authorDropdown+"|"+"Book_by_Genre-"+genreDropdown+"|book_type-"+typeDropdown };
  console.log(requestData);
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    // Process the response data
    console.log(data);
    displayImages(data.imageUrls, data.titles, data.authors, data.types, data.genres);

  })
  .catch(function(error) {
    console.error("Error:", error);
  });
});

clearButton.addEventListener("click", function(event) {
  event.preventDefault(); // Prevent form submission
  var inputString = document.getElementById("inputString").value;
  var url = "/api/images";
  
  var requestData = { inputString: inputString };
  console.log(requestData);
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    // Process the response data
    console.log(data);
    displayImages(data.imageUrls, data.titles, data.authors, data.types, data.genres);

  })
  .catch(function(error) {
    console.error("Error:", error);
  });
});


function displayImages(imageUrls, titles, authors, types, genres) {
  var imageGrid = document.getElementById("image-grid");
  imageGrid.innerHTML = ""; // Clear existing images

  var metadataPromises = []; // Array to store metadata fetch promises
  if (imageUrls.length != 0){
    for (let i = 0; i < imageUrls.length; i++) {
      var imageWrapper = document.createElement("div");
      imageWrapper.className = "image-wrapper";

      var image = document.createElement("img");
      image.src = imageUrls[i];
      image.className = "image";
      image.addEventListener("mouseenter", function() {
        this.parentElement.querySelector(".overlay").style.opacity = "1";
      });
      image.addEventListener("mouseleave", function() {
        this.parentElement.querySelector(".overlay").style.opacity = "0";
      });
       //adding code for rating of books
       var imageUrls = imageUrls
      imageWrapper.addEventListener("click", function() {
        var apiUrl = "/api/book-details";
        var requestData = { imageUrl: imageUrls[i] }; // Use closure to capture the value of i
        console.log(i)
        fetch(apiUrl, {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
        return response.text();
        })
        .then(function(data) {
            var newWindow = window.open();
            newWindow.document.open();
            newWindow.document.write(data);
            newWindow.document.close();
            })
            .catch(function(error) {
            console.error("Error:", error);
            });
        });


      var overlay = document.createElement("div");
      overlay.className = "overlay";

      var details = document.createElement("div");
      details.className = "details";

      var author = document.createElement("p");
      author.textContent = "Author: ";

      var genre = document.createElement("p");
      genre.textContent = "Genre: ";

      details.appendChild(author);
      details.appendChild(genre);
      overlay.appendChild(details);

      var title = document.createElement("p");
      title.textContent = titles[i];
      title.className = "title";

      imageWrapper.appendChild(image);
      imageWrapper.appendChild(overlay);
      imageWrapper.appendChild(title);
      imageGrid.appendChild(imageWrapper);

      // Call another API to fetch metadata
      var metadataPromise = fetchMetadata(imageUrls[i], author, genre);
      metadataPromises.push(metadataPromise);
    }

    // Wait for all metadata fetch requests to resolve
    Promise.all(metadataPromises)
      .then(function() {
        // Show the image grid
        imageGrid.style.display = "block";

        var greenPanel = document.getElementById("green-panel");
        greenPanel.style.display = "block";

        // Populate type dropdown
        var typeDropdown = document.getElementById("type-dropdown");
        populateDropdown(typeDropdown, types);

        // Populate genre dropdown
        var genreDropdown = document.getElementById("genre-dropdown");
        populateDropdown(genreDropdown, genres);

        // Populate author dropdown
        var authorDropdown = document.getElementById("author-dropdown");
        populateDropdown(authorDropdown, authors);
      })
      .catch(function(error) {
        console.error("Error:", error);
      });
    }
    else {
    displayError("No results to display.");
  }
}

function displayError(message) {
  var errorElement = document.getElementById("image-grid");
  errorElement.textContent = message;
  errorElement.style.display = "block";
}

function populateDropdown(dropdown, options) {
  while (dropdown.firstChild) {
        dropdown.removeChild(dropdown.firstChild);
      }
  options.forEach(function(option) {
    var optionElement = document.createElement("option");
    optionElement.value = option;
    optionElement.textContent = option;
    dropdown.appendChild(optionElement);
  });
}

function fetchMetadata(imageUrl, authorElement, genreElement) {
  var metadataUrl = "/api/metadata";
  var requestData = { imageUrl: imageUrl };
  return fetch(metadataUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    // Process the metadata response data
    console.log(data);
    // Update the metadata elements
    authorElement.textContent += data.author;
    genreElement.textContent += data.genre;
  })
  .catch(function(error) {
    console.error("Error:", error);
  });
}
