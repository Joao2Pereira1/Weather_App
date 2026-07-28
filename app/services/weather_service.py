"""
WeatherService for the weather application.

This module handles the request to the weather api, to get the forecast
of the weather in a specific location for the next 7 days and it also formats
 and returns the weather data, so it can be used in the main window controller.
"""

import datetime
import json

import requests  # type: ignore
from model.weather_data import LocationData, WeatherData

WEEK_DAYS_TRANSLATOR = {
    "Monday": "Segunda",
    "Tuesday": "Terça",
    "Wednesday": "Quarta",
    "Thursday": "Quinta",
    "Friday": "Sexta",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

WEEK_DAYS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


class WeatherService:
    """class responsible to do the request to weather api, and
    formatting data to be able to use it after."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.content = None

    def fetch_forecast(self, local: str) -> bool:
        """
        Makes a request to the API to get forecast data for the next week.

        Args:
            local (str): Location name (not case sensitive).

        Returns:
            bool:
                True if the request was successful and the content was stored.
                False if the request failed.
        """

        url = (
            "https://api.weatherapi.com/v1/forecast.json"
            f"?key={self.api_key}"
            f"&q={local}"
            "&days=7"
            "&aqi=no"
            "&alerts=no"
        )

        try:
            response = requests.get(
                url,
                timeout=10,
            )

            response.raise_for_status()

        except requests.exceptions.Timeout:
            self.error_message = (
                "Tempo limite excedido. Verifique a ligação à internet."
            )
            return False

        except requests.exceptions.ConnectionError:
            self.error_message = "Sem ligação à internet."
            return False

        except requests.exceptions.HTTPError:
            self.error_message = self._get_api_error(response)
            return False

        except requests.exceptions.RequestException as error:
            self.error_message = f"Erro ao contactar a API: {error}"
            return False

        try:
            self.content = response.json()

        except ValueError:
            self.error_message = "Resposta inválida recebida da API."
            return False

        return True

    def _get_api_error(self, response: requests.Response) -> str:
        """
        Converts API errors into user-friendly messages.
        Returns:
            str: Error message.
        """

        try:
            error_code = response.json()["error"]["code"]

        except (ValueError, KeyError):
            return "Erro desconhecido na API."

        errors = {
            1006: "Localização não encontrada.",
            2006: "Chave API inválida.",
            2007: "Limite da API excedido.",
            9999: "Erro interno da API.",
        }

        return errors.get(
            error_code,
            "Erro ao obter dados meteorológicos.",
        )

    def get_location_info(self) -> LocationData | None:
        """
        Returns more details about the location.

        Returns:
            LocationData: class with attributes name,region, country e hour.

            None: if no content is available.
        """

        if not self.content:
            return None

        # info about local selected and hour
        location = self.content["location"]

        return LocationData(
            name=location["name"],
            region=location["region"],
            country=location["country"],
            local_time=location["localtime"],
        )

    def get_forecast(self) -> tuple[str, dict[str, WeatherData]] | None:
        """
        Returns the forecast weather to the next 7 days.

        Returns:
            tuple: (actual_day, forecast), where:
                - actual_day (str): day of the week, e.g., "Monday".
                - forecast (dict): {"YYYY-MM-DD": [max, min, average, condition, icon]}.

            None: if no content is available
        """

        if not self.content:
            return None

        # forecast_day it will be a list with the forecast for 7 days
        forecast_list = self.content["forecast"]["forecastday"]
        forecast_dict = {}

        current_day = datetime.date.today().strftime("%A")  # returns monday,tuesday,...
        current_day = WEEK_DAYS_TRANSLATOR[current_day]  # translates to portuguese

        # each item on the list represents the forecast for that day
        for item in forecast_list:
            day_info = item["day"]
            forecast_dict[item["date"]] = WeatherData(
                date=item["date"],
                max_temp=day_info["maxtemp_c"],
                min_temp=day_info["mintemp_c"],
                avg_temp=day_info["avgtemp_c"],
                state=day_info["condition"]["text"],
                icon_url=day_info["condition"]["icon"],
            )
        return current_day, forecast_dict
