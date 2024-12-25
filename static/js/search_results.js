let debounceTimeout;
document.getElementById("search-input").addEventListener("input", function () {
  clearTimeout(debounceTimeout);
  const query = this.value;
  if (query.length > 2) {
    debounceTimeout = setTimeout(() => {
      fetch(`/search_suggestions?q=${query}`)
        .then((response) => response.json())
        .then((data) => {
          const suggestions = document.getElementById("suggestions");
          suggestions.innerHTML = "";
          data.forEach((item) => {
            const li = document.createElement("li");
            const link = document.createElement("a");
            link.textContent = item.title;
            link.href = `/question/${item.id}`;
            li.appendChild(link);
            suggestions.appendChild(li);
          });
          suggestions.style.display = "block";
        });
    }, 300);
  } else {
    document.getElementById("suggestions").style.display = "none";
  }
});

document.addEventListener("click", function (event) {
  if (!document.getElementById("search-input").contains(event.target)) {
    document.getElementById("suggestions").style.display = "none";
  }
});
