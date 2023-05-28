document.getElementById("myForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submission
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
    displayImages(data.imageUrls, data.titles,data.authors,data.types,data.genres);
  })
  .catch(function(error) {
    console.error("Error:", error);
  });
});

function displayImages(imageUrls, titles, authors, types, genres) {
  var imageGrid = document.getElementById("image-grid");
  imageGrid.innerHTML = ""; // Clear existing images

  var metadataPromises = []; // Array to store metadata fetch promises

  for (var i = 0; i < imageUrls.length; i++) {
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

function populateDropdown(dropdown, options) {
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
  fetch(metadataUrl, {
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

