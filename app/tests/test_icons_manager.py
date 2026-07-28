from pathlib import Path

import pytest  # type:ignore

from app.utils.icons_manager import IconsManager


@pytest.fixture
def icons_manager(tmp_path):
    """Creates a fresh instance of IconsManager before each test"""

    icons_folder = tmp_path / "icons"
    dict_file = tmp_path / "icons_dict.txt"
    return IconsManager(folder_path=str(icons_folder), dict_path=str(dict_file))

def test_load_dict_existing_file(tmp_path):
    """Creates a new dictionary in another file, then inserts an element
    like sunny: app/... and checks if the IconsManager loads the file correctly """

    dict_file = tmp_path / "icons_dict.txt"
    dict_file.write_text("Sunny,app/icons/sunny.png\n", encoding="utf-8")
    manager = IconsManager(folder_path=str(tmp_path), dict_path=str(dict_file))
    assert manager.weather_icons == {"Sunny": "app/icons/sunny.png"}

def test_load_dict_no_file(icons_manager):
    """Verify in case the dict file doesn't exist, if the result is {} """

    result = icons_manager.load_dict()
    assert result == {}

def test_save_dict(icons_manager):
    """Check if the dictionary is saved correctly in the temporary path """

    icons_manager.weather_icons = {"Sunny": "app/icons/sunny.png"}
    icons_manager.save_dict()
    content = Path(icons_manager.dict_path).read_text(encoding="utf-8")
    assert "Sunny,app/icons/sunny.png" in content

def test_get_icon_from_cache(icons_manager):
    """Try to get an icon using the get_weather_icon_path method,
    it's passed a /invalid/url cause it doesn't matter """

    icons_manager.weather_icons = {"Sunny": "app/icons/sunny.png"}
    result = icons_manager.get_weather_icon_path("Sunny", "/invalid/url")
    assert result == "app/icons/sunny.png"
