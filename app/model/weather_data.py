from dataclasses import dataclass


@dataclass
class WeatherData:
    date: str
    max_temp: float
    min_temp: float
    avg_temp: float
    state: str
    icon_url: str

@dataclass
class LocationData:
    name: str
    region: str
    country: str
    local_time: str


    def __str__(self):
        return f"Detalhes do local -> Nome: {self.name}, Região: {self.region}, País: {self.country}, Hora: {self.local_time}"
