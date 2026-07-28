# 🌤️ Weather App

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A desktop application built in **Python** with **PyQt5**, consuming the **WeatherAPI** to deliver detailed weather forecasts in a fast and optimized way. The project follows solid software architecture practices, implements local caching for assets (icons) to avoid unnecessary network requests, and features a responsive, modern graphical interface.

## Overview & Functionality

This application is a practical desktop project designed to test API integration, JSON data parsing, image asset caching, and GUI creation using Qt.

- **Core Feature:** The user inputs a specific location. Upon submission, the app dynamically extracts the location name, country, and current local time.
- **Forecast Display:** The application displays the current weather data for today plus a 6-day forward forecast (7 days total).
- **Data Optimization:** Because the API's full forecast payload is massive (containing hourly data), the application parses and displays only the essential daily summary: maximum, minimum, and average temperatures, alongside the general weather condition status and corresponding visual icons.

---

## User Interface (Qt)

The graphical user interface was initially designed visually using **Qt Designer** and subsequently customized through code adjustments.

### Interface Architecture (Main Window)

```
MainWindow
│
├── menubar (Top Menu)
│   ├── weatherMenu
│   │   ├── actionRefresh
│   │   ├── actionCurrentLocation
│   │   └── actionExit
│   │
│   └── helpMenu
│       ├── actionHelp
│       └── actionAbout
│
├── statusbar
│   └── statusLabel (QLabel) -> Displays "Ready" or loading states
│
└── centralwidget
    │
    └── mainLayout
        │
        ├── searchLayout
        │   ├── locationLabel
        │   ├── locationInput
        │   └── searchButton
        │
        ├── locationInfoLabel (Metadata: City, Country, and Local Time)
        │
        ├── forecastTitle
        │
        └── weekLayout (7-Day Forecast Panel)
            ├── card_1 (Today's Forecast)
            ├── card_2 (Tomorrow's Forecast)
            ├── ...
            └── card_7 (7th Day Forecast)
```

### Key UI Workflows

- **Location Lookup:** The user types a city name into `locationInput` and clicks `searchButton`. The `local` value (e.g., `"aveiro"`) is used to update the query parameters.
- **Automatic Location Detection:** The "Current Location" menu item/button uses utility services to detect the user's coordinates or IP address and perform the lookup automatically.
- **JSON Data Extraction:** Parses the nested JSON response to extract string values for the location name, country, and local time, as well as array data for the 7 forecast days.
- **Forecast Cards:** Each of the 7 forecast cards displays:
  - The corresponding day of the week.
  - Expected maximum, minimum, and average temperatures.
  - The weather condition icon (loaded locally via the cache manager).
  - The general condition status (e.g., "Light rain", "Sunny").
- **Visual Layout:** Organizes text data and pairs them with their locally-cached weather icons across the dashboard.

---

## Project Structure

The folder and file organization follows the **MVC (Model-View-Controller)** pattern to decouple business logic, interface, and data-consuming services.

```
app/
│
├── controller/
│   └── main_window_controller.py   # Connects the UI to services, handles events, updates, and data population
│
├── model/
│   ├── weather_data.py             # Data structures (WeatherData and LocationData classes)
│   └── icons_dict.txt              # Mapping of weather conditions to icons
│
├── services/
│   └── weather_service.py          # Performs HTTP calls to the API, handles errors, and converts responses into Model instances
│
├── ui/
│   ├── gui.py                      # Interface code generated from Qt Designer
│   └── gui.ui                      # Qt Designer visual design XML file
│
├── utils/
│   ├── convert_timezone.py         # Utility for formatting and converting times and timezones
│   ├── get_current_location.py     # Utility for determining the user's current location
│   ├── icons_manager.py            # Responsible for downloading and locally caching weather icons
│   ├── request.py                  # Wraps standard HTTP requests with exception handling
│   └── example.json                # Sample API JSON payload for offline testing
│
├── docs/
│   ├── api usada.txt               # Reference links and API keys
│   ├── explicacao api.txt          # Quick guide to payloads and endpoints
│   ├── styles.txt                  # Color palette and CSS/QSS stylesheets used in the interface
│   └── WARNING.txt                 # Notes on PyQt5 version compatibility
│
├── icons/                          # Folder where cached weather icons are stored
│   ├── sunny.png
│   ├── cloudy_.png
│   ├── heavy_rain.png
│   └── ...                         # Icons downloaded dynamically on demand
│
├── tests/
│   ├── test_api.py                 # Unit tests for API endpoints
│   ├── test_icons_manager.py       # Tests for the icon download and caching flow
│   ├── test_weather_service.py     # Integration tests for data fetching and processing
│   └── __init__.py
│
├── main.py                         # Application entry point that starts the Qt event loop
├── requirements.txt                # Dependencies required to run the project
└── .env                            # Environment variables (e.g., API key — not included for security reasons)
```

---

## API Architecture

While WeatherAPI offers multiple endpoints (such as `/current.json`, `/search.json`, `/history.json`, and `/alerts.json`), this application exclusively implements the **Forecast** method to gather all required real-time and future data in a single request — reducing latency and network traffic.

### Implemented API Method

- **Endpoint:** `/forecast.json`
- **Purpose:** Used to retrieve both the current local metadata and the upcoming 7-day weather outlook.

### Request Parameters

| Parameter | Required | Description |
|---|---|---|
| `key` | Yes | Your unique WeatherAPI developer key. |
| `q` | Yes | The query location parameter, passed dynamically based on the user's city choice (e.g., `q={local}`). |
| `days` | No | Set to `7` to fetch today's weather and the 6 subsequent days. |
| `aqi` | No | Air Quality Index flag. Set to `no` to keep data payloads light. |
| `alerts` | No | Weather alerts flag. Set to `no` since severe alerts are not required for this implementation. |

#### Dynamic Request Example

```python
f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={local}&days=7&aqi=no&alerts=no"
```

---

## Image Asset Management (Icons Cache)

To display weather conditions visually without degrading application performance, the project includes a dedicated component called `icons_manager`.

- **The Problem:** Each weather state comes with an icon URL from the API. Making a network request to download the image file every single time the UI refreshes would flood the network and slow down the interface.
- **The Solution (`icons_manager`):**
  1. Extracts the icon asset link from the API's JSON response.
  2. Checks if the image file already exists in the local `icons/` directory.
  3. **Cache Miss:** If the image is not local, it downloads the raw binary content of the icon and saves it locally.
  4. **Cache Hit:** If the image already exists locally, it skips the network entirely and loads it immediately.
  5. Finally, it renders the image smoothly inside the Qt application layout.

---

## Requirements & Setup

### System Requirements

- **Python:** >= 3.8 (Note: PyQt5 has packaging limitations on very recent Python versions without the correct compiler; see `docs/WARNING.txt`.)

### Installing Dependencies

Project dependencies are declared in `requirements.txt`:

```
pyqt5
requests
python-dotenv
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## How to Run the Project

1. **Get an API key:** Sign up for free at [WeatherAPI](https://www.weatherapi.com/) to obtain your access key.
2. **Set up environment variables:** Create a `.env` file in the project root and configure your secret key:

   ```
   WEATHER_API_KEY=your_key_here
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

---

# License

This project is distributed under the MIT License.
