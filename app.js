const API_KEY = '5f974f5fe2e70a2764bc875d31e2c3ad';
const getWeatherBtn = document.getElementById('getWeatherBtn');
const cityInput = document.getElementById('cityInput');
const weatherResult = document.getElementById('weatherResult');

getWeatherBtn.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (!city) return;

    fetchWeatherData(city);
});


async function fetchWeatherData(city) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`);
        const data = await response.json();

        if (data.cod === 200) {
            const weatherDescription = data.weather[0].description;
            const temperature = data.main.temp;
            // const wind_speed = response['wind']['speed']
            // const humidity =response['main']['humidity']
            // const description = response['weather'][0]['description']
            // const sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            // const sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

            weatherResult.innerHTML = `<p>Weather: ${weatherDescription}</p><p>Temperature: ${temperature}°C</p>`;
        } else {
            weatherResult.innerHTML = `<p>City not found. Please try again.</p>`;
        }
    } catch (error) {
        console.error('Error fetching weather data:', error);
        weatherResult.innerHTML = `<p>Something went wrong. Please try again later.</p>`;
    }
}
