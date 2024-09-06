document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    const searchResults = document.getElementById('search-results');

    searchInput.addEventListener('input', debounce(function() {
        const query = this.value.trim();
        if (query.length > 2) {
            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.innerHTML = '';
                    searchResults.classList.remove('hidden');
                    data.forEach(leader => {
                        const div = document.createElement('div');
                        div.classList.add('search-result', 'p-2', 'hover:bg-gray-100');
                        div.innerHTML = `
                            <a href="/profile/${leader.id}" class="block">
                                <div class="font-semibold">${leader.name}</div>
                                <div class="text-sm text-gray-600">${leader.company}</div>
                            </a>
                        `;
                        searchResults.appendChild(div);
                    });
                    if (data.length === 0) {
                        searchResults.innerHTML = '<div class="p-2">No results found</div>';
                    }
                });
        } else {
            searchResults.innerHTML = '';
            searchResults.classList.add('hidden');
        }
    }, 300));

    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
            searchResults.classList.add('hidden');
        }
    });
});

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}
