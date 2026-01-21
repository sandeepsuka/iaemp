function loadHTML(id, file) {
  fetch(file)
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to load " + file);
      }
      return response.text();
    })
    .then(data => {
      document.getElementById(id).innerHTML = data;
    })
    .catch(error => {
      console.error(error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  loadHTML("site-header", "/assets/partials/header.html");
  loadHTML("site-footer", "/assets/partials/footer.html");
});
