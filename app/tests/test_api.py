import pytest  # type: ignore
import requests  # type: ignore
import requests_mock  # type: ignore
import os
from dotenv import load_dotenv

### Uso básico da API

# url = "https://api.weatherapi.com/v1/current.json?key={api_key}&q=London&aqi=no"
# request = requests.get(url)  # nosec

# print(f"\nStatus code: {request.status_code}\n\n")
# print(f"Headers: {request.headers}\n\n")
# print(f"Content: {request.content}\n\n")
# print(f"Text: {request.text}\n")

load_dotenv()
api_key = os.getenv("API_KEY")


def get_weather_data(city: str) -> dict:
    """Busca os dados sobre o tempo para uma cidade específica."""
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    response = requests.get(url, timeout=5)

    # Levanta uma excecao caso a API retorne um erro (ex: 400, 401, 500)
    response.raise_for_status()

    return response.json()


# --- Casos de Teste com Pytest e Mocking ---


def test_get_weather_data_success():
    """Caso 1: Sucesso total da API (Status 200) com dados esperados."""
    city = "London"
    api_url = (
        f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    )

    # Mock do JSON que a API real devolveria
    mock_response_payload = {
        "location": {"name": "London", "country": "United Kingdom"},
        "current": {"temp_c": 18.0, "condition": {"text": "Partly cloudy"}},
    }

    # Ativando o mock para esta requisicao específica
    with requests_mock.Mocker() as mock:
        mock.get(api_url, json=mock_response_payload, status_code=200)

        # Executa a funcao
        result = get_weather_data(city)

        # Validacoes (Asserts)
        assert result["location"]["name"] == "London"
        assert result["current"]["temp_c"] == 18.0
        assert mock.called  # Garante que a requisicao foi de fato simulada


def test_get_weather_data_invalid_api_key():
    """Caso 2: Erro de autenticacao (Status 401 - Chave Inválida)."""
    city = "London"
    api_url = (
        f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    )

    with requests_mock.Mocker() as mock:
        # Simulando que a API rejeitou a API Key
        mock.get(api_url, status_code=401)

        # O pytest garante que a excecao do requests será levantada corretamente
        with pytest.raises(requests.exceptions.HTTPError):
            get_weather_data(city)


def test_get_weather_data_city_not_found():
    """Caso 3: Cidade nao encontrada (Status 400)."""
    city = "CidadeInexistente"
    api_url = (
        f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    )

    with requests_mock.Mocker() as mock:
        mock.get(api_url, status_code=400)

        with pytest.raises(requests.exceptions.HTTPError):
            get_weather_data(city)


def test_get_weather_data_timeout():
    """Caso 4: A API falhou por Timeout (Falta de resposta/queda de conexao)."""
    city = "London"
    api_url = (
        f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    )

    with requests_mock.Mocker() as mock:
        mock.get(api_url, exc=requests.exceptions.Timeout)

        with pytest.raises(requests.exceptions.Timeout):
            get_weather_data(city)
