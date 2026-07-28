import requests  # type: ignore
import os
from dotenv import load_dotenv


def get_temperature(local) -> float:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={local}&days=7&aqi=no&alerts=no"

    response = requests.get(url)  # nosec

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Error")


if __name__ == "__main__":
    get_temperature("Salreu")
