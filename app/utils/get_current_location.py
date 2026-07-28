import requests


def get_current_location():
    """
    Obtém a cidade atual através do endereço IP.
    Retorna o nome da cidade ou None em caso de erro.
    """

    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        response.raise_for_status()

        data = response.json()

        if data["status"] == "success":
            return data["city"]

    except requests.RequestException:
        pass

    return None
