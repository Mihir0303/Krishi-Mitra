let id = '9b334975b0909addc87bf73989d99271';  // Replace with your actual OpenWeatherMap API key
let url = 'https://api.openweathermap.org/data/2.5/weather?units=metric&appid=' + id;

let city = document.querySelector('.name');
let form = document.querySelector("form");
let temperature = document.querySelector('.temperature');
let description = document.querySelector('.description');
let valueSearch = document.getElementById('name');
let clouds = document.getElementById('clouds');
let humidity = document.getElementById('humidity');
let pressure = document.getElementById('pressure');
let main = document.querySelector('main');

form.addEventListener("submit", (e) => {
    e.preventDefault();  
    if(valueSearch.value != '') {
        searchWeather();
    }
});

// Function to get the user's location and fetch weather data
const getLocationAndWeather = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // Reverse geocode using OpenStreetMap's Nominatim API to get the address
            let geoUrl = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`;

            fetch(geoUrl)
                .then(response => response.json())
                .then(data => {
                    const cityName = data.address.city || data.address.town || data.address.village;
                    console.log(`City: ${cityName}`);
                    
                    // Now search for weather data using the city from reverse geocoding
                    if (cityName) {
                        valueSearch.value = cityName;
                        searchWeather();
                    } else {
                        console.log("Unable to get city name");
                    }
                })
                .catch(error => {
                    console.error('Error getting address:', error);
                });
        }, (error) => {
            console.error("Error fetching location:", error);
        });
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
};

// Function to fetch the weather data from OpenWeatherMap
const searchWeather = () => {
    fetch(url + '&q=' + valueSearch.value)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.cod == 200) {
                // Update the page with the weather data
                city.querySelector('figcaption').innerHTML = data.name;
                city.querySelector('img').src = `https://flagsapi.com/${data.sys.country}/shiny/32.png`;
                temperature.querySelector('img').src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@4x.png`;
                temperature.querySelector('span').innerText = data.main.temp;
                description.innerText = data.weather[0].description;

                clouds.innerText = data.clouds.all;
                humidity.innerText = data.main.humidity;
                pressure.innerText = data.main.pressure;
            } else {
                main.classList.add('error');
                setTimeout(() => {
                    main.classList.remove('error');
                }, 1000);
            }
            valueSearch.value = '';
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
}

// Default search on page load (use the user's location)
const initApp = () => {
    getLocationAndWeather();
}

// Initialize the app when the page loads
initApp();
