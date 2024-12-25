const searchInput = document.getElementById('search-input');
const suggestionsDropdown = document.getElementById('suggestions-dropdown');

let timeoutId;

searchInput.addEventListener('input', function(event) {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
        const query = event.target.value;

        if (query.length > 2) {
          fetch(`/search_suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
              suggestionsDropdown.innerHTML = '';
              if (data.suggestions.length > 0) {
                data.suggestions.forEach(suggestion => {
                  const suggestionItem = document.createElement('a');
                  suggestionItem.href = suggestion.url;
                  suggestionItem.textContent = suggestion.title;
                  suggestionsDropdown.appendChild(suggestionItem);
                });
                suggestionsDropdown.style.display = 'block';
              } else {
                suggestionsDropdown.style.display = 'none';
              }
            });
        } else {
          suggestionsDropdown.style.display = 'none';
        }
    }, 300);
});


searchInput.addEventListener('blur', function() {
    setTimeout(() => {
      suggestionsDropdown.style.display = 'none';
    }, 200);
});
