import datetime
from services import weather_service

"""
Por exemplo se pesquisares japao, devido ao desfasamento de horário,
no japao ja pode ser quarta e como usava a data do computador, ia
aparecer terca em vez de quarta
"""

weather_service.WEEK_DAYS


def translate_weekday(date_string: str) -> str:

    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")

    english_day = date.strftime("%A")

    return weather_service.WEEK_DAYS[english_day]
