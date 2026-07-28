"""
Main window controller for the weather application.

This module handles the interaction between the UI components and the
business logic, updating widgets with weather data, handling user input,
and managing signals and slots for the main application window.
"""

from typing import List

from utils.get_current_location import get_current_location
from model.weather_data import WeatherData
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow, QMessageBox
from services.weather_service import WEEK_DAYS, WeatherService
from ui.gui import Ui_MainWindow  # UI design for the application
from utils.icons_manager import IconsManager
import os
from dotenv import load_dotenv


class MainWindowController(QMainWindow):
    """Main window controller will be responsible to update
    the gui when something happens."""

    def __init__(self):
        """
        self → the main window (QMainWindow) that will be displayed on the screen.
        Ui_MainWindow → the interface class created in Qt Designer.

        self.ui.setupUi(self) → method of the Ui_MainWindow class
        that takes a window (QMainWindow) as an argument and is responsible
        for adding the widgets created in Qt Designer
        into the main window (self).
        """
        load_dotenv()
        api_key = os.getenv("API_KEY")

        super().__init__()  # inherits QMainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ? Gerir eventos
        self.ui.searchButton.clicked.connect(self.retrieve_weather_data)

        # < Instancias das classes
        self.weather_service = WeatherService(api_key)
        self.icons_manager = IconsManager()

        # ! Funções para cada opcao na menubar Menu Clima e Acerca de

        # Menu Clima
        self.ui.actionRefresh.triggered.connect(self.refresh_pressed)
        self.ui.actionCurrentLocation.triggered.connect(self.current_location_pressed)
        self.ui.actionExit.triggered.connect(self.close)

        # Menu Acerca de
        self.ui.actionHelp.triggered.connect(self.help_pressed)
        self.ui.actionAbout.triggered.connect(self.about_pressed)

        # When pressing return key, retrieve data
        self.ui.locationInput.returnPressed.connect(self.retrieve_weather_data)

        # objetos da ui
        self.days: List[QLabel] = [
            self.ui.day_1,
            self.ui.day_2,
            self.ui.day_3,
            self.ui.day_4,
            self.ui.day_5,
            self.ui.day_6,
            self.ui.day_7,
        ]
        self.icons: List[QLabel] = [
            self.ui.icon_1,
            self.ui.icon_2,
            self.ui.icon_3,
            self.ui.icon_4,
            self.ui.icon_5,
            self.ui.icon_6,
            self.ui.icon_7,
        ]
        self.temperatures: List[QLabel] = [
            self.ui.temperature_1,
            self.ui.temperature_2,
            self.ui.temperature_3,
            self.ui.temperature_4,
            self.ui.temperature_5,
            self.ui.temperature_6,
            self.ui.temperature_7,
        ]

    # Functions for each item in menubar Clima de refresh, currentLocation e exit

    def refresh_pressed(self):
        """Updates weather data, by using the local inserted."""

        self.retrieve_weather_data()

    def current_location_pressed(self):
        """Get current location and retrieves weather data for the location obtained."""

        city = get_current_location()

        if city:
            self.ui.locationInput.setText(city)
            self.retrieve_weather_data()
        else:
            QMessageBox.warning(
                self, "Erro", "Não foi possível obter a localização atual."
            )

    def exit_pressed(self):
        self.close()

    # Functions for each item in menubar Acerca de help e about

    def help_pressed(self):
        message = QMessageBox(self)
        message.setText(
            "Para ajuda verifique a documentação ou entre em contacto: https://github.com/Joao2Pereira1/Learning-Projects/tree/main/WeatherApp"
        )
        message.exec()

    def about_pressed(self):
        message = QMessageBox(self)
        message.setText(
            "Isto é uma simples aplicação que mostra a previsão do clima nos próximos 7 dias."
        )
        message.exec()

    def retrieve_weather_data(self) -> None:
        """It will receive the local input and then show the data at GUI.
        Local Input is the LineEdit responsible to get city or place.
        """

        # print("Botao clicado!")

        local = self.ui.locationInput.text()
        response = self.weather_service.fetch_forecast(local)

        if response:
            location_data = self.weather_service.get_location_info()
            self.ui.locationInfoLabel.setText(str(location_data))

            # returns a tuple(current day, dictionary with weather data for each day)
            current_day, forecast = self.weather_service.get_forecast()

            day: str
            weather: WeatherData

            # get current day index in WEEK_DAYS
            day_index = WEEK_DAYS.index(current_day)

            print(forecast.items)
            # show data about the forecast -> [day: weather data]
            i = 0
            for day, weather in forecast.items():
                print(weather)
                if day_index == 7:
                    day_index = 0
                    self.days[i].setText(f"{day}\n  {WEEK_DAYS[day_index]}")
                else:
                    self.days[i].setText(f"{day}\n  {WEEK_DAYS[day_index]}")
                icon_path = self.icons_manager.get_weather_icon_path(
                    weather.state, weather.icon_url
                )
                self.icons[i].setPixmap(QPixmap(icon_path))
                self.temperatures[i].setText(f"{weather.min_temp}  {weather.max_temp}")
                i += 1
                day_index += 1
        else:
            alert = QMessageBox(self)
            alert.setText("Local inserido inválido.")
            alert.exec()
            self.ui.locationInput.setText("")
            print("Local inserido inválido.")
