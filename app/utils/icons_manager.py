"""
IconsManager module for the weather application.

This module handles the download and local storage of weather condition icons.
Icons are cached locally to avoid repeated network requests, improving performance
and reducing unnecessary API calls.
"""

import pathlib
import requests  # type: ignore


class IconsManager:
    """
    Responsible to manage icons dictionary:
    - Verifies if icon is saved locally.
    - Does the download from request url and saves new icons locally.
    -> Basically it serves as cache to improve performance.
    """

    def __init__(
        self,
        folder_path: str = "icons",
        dict_path: str = "icons_dict.txt",
    ):
        base_path = pathlib.Path(__file__).resolve().parent.parent

        self.icons_folder = base_path / folder_path
        self.dict_path = base_path / dict_path

        self.icons_folder.mkdir(parents=True, exist_ok=True)

        self.weather_icons = self.load_dict()

    def load_dict(self) -> dict:
        """
        Loads dictionary from the file, because when the program
        resets, it looses the dictionary data.

        Returns:
            Dict: to check if operation was successful.
        """

        weather_icons = {}

        if not self.dict_path.exists():
            return weather_icons

        try:
            with open(self.dict_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    icon, path = line.split(",", 1)
                    weather_icons[icon] = path

        except (OSError, ValueError):
            return {}

        return weather_icons

    def save_dict(self) -> bool | str:
        """
        Saves dictionary: dict{"sunny":"icons/sunny.png"}.

        Returns:
            Message: to check if operation was successful.
        """

        try:
            with open(self.dict_path, "w", encoding="utf-8") as f:
                for icon, path in self.weather_icons.items():
                    f.write(f"{icon},{path}\n")  # separado por virgula
            return True
        except FileNotFoundError as e:
            message = f"Couldn't find file to save dictionary:{e}"
        except PermissionError as e:
            message = f"No permission to save dictionary in this file:{e}"
        return message

    def get_weather_icon_path(
        self, weather_state: str, weather_icon_url: str
    ) -> str | None:
        """
        Responsible to get the icons associated to the weather state,
        if it's present in the dictionary, otherwise new icon is added.

        Args:
            weather_state (str): weather state, if it's sunny, rainy, ...
            weather_icon_url(str):  icon url to do the request to save the icon png.
        Raises:
            Exception: in case the file is not downloaded.
        Returns:
            str: The local path to the saved icon, so it can be loaded in the GUI.

            None: in case it happened some error.
        """

        filename = weather_state.lower().replace(" ", "_") + ".png"
        icon_path = self.icons_folder / filename

        # Check existing cache
        if weather_state in self.weather_icons:

            cached_path = pathlib.Path(self.weather_icons[weather_state])

            if cached_path.exists():
                return str(cached_path)

            # Cache entry exists but file disappeared
            del self.weather_icons[weather_state]

        try:
            url = (
                weather_icon_url
                if weather_icon_url.startswith("http")
                else f"https:{weather_icon_url}"
            )

            response = requests.get(
                url,
                timeout=10,
            )

            response.raise_for_status()

        except requests.RequestException:
            return None

        # Validate image data
        if not response.content.startswith(b"\x89PNG"):
            return None

        try:
            with open(icon_path, "wb") as file:
                file.write(response.content)

        except OSError:
            return None

        self.weather_icons[weather_state] = str(icon_path)
        self.save_dict()

        return str(icon_path)
