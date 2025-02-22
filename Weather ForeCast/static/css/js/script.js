// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Auto-detect user's location
    document.getElementById('detect-location').addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(fetchWeatherByCoords, showError);
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    });

    // Auto-complete cities
    const cityInput = document.getElementById('city-input');
    cityInput.addEventListener('input', function(e) {
        const query = e.target.value;
        if (query.length > 2) {
            fetch(`/autocomplete?query=${query}`)
                .then(response => response.json())
                .then(data => showSuggestions(data));
        }
    });
});

function fetchWeatherByCoords(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    window.location.href = `/weather?lat=${lat}&lon=${lon}`;
}

function showError(error) {
    alert(`Error: ${error.message}`);
}

function showSuggestions(cities) {
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = cities.map(city => `
        <div class="suggestion-item" onclick="selectCity('${city.name}, ${city.country}')">
            ${city.name}, ${city.country}
        </div>
    `).join('');
}

function selectCity(city) {
    document.getElementById('city-input').value = city;
    document.getElementById('suggestions').innerHTML = '';
}