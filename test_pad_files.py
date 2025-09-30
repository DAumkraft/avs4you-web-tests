import pytest
import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
import yaml


# Словарь соответствия product_name из data.yaml и имён файлов PAD
PAD_FILE_MAPPING = {
    "avs_video_remaker": "AVSVideoReMaker",
    "avs_video_editor": "avsvideoeditor",
    "avs_video_converter": "avsvideoconverter",
    "avs_audio_converter": "AVSAudioConverter",
    "avs_audio_editor": "AVSAudioEditor",
    "avs_media_player": "AVSMediaPlayer",
    "avs_image_converter": "avsimageconverter",
    "avs_photo_editor": "AVSphotoEditor"
}

# Языки PAD-файлов
PAD_LANGUAGES = ["en", "de"]


@pytest.fixture(scope="module")
def driver():
    """Chrome драйвер в headless режиме"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def load_editor_data(product_name):
    """Загружает данные продукта из data.yaml"""
    with open("data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["products"][product_name]


def get_pad_data(pad_url):
    """Получает и парсит данные из PAD XML файла"""
    try:
        response = requests.get(pad_url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        pad_data = {}

        # Название программы
        program_name = root.find(".//Program_Name")
        if program_name is not None:
            pad_data["name"] = program_name.text.strip()

        # Версия
        program_version = root.find(".//Program_Version")
        if program_version is not None:
            pad_data["version"] = program_version.text.strip()

        # Размер в MB
        file_size_mb = root.find(".//File_Size_MB")
        if file_size_mb is not None:
            pad_data["size"] = f"{file_size_mb.text.strip()} MB"

        # Размер в байтах
        file_size_bytes = root.find(".//File_Size_Bytes")
        if file_size_bytes is not None:
            pad_data["size_bytes"] = int(file_size_bytes.text.strip())

        # Размер в килобайтах
        file_size_kilobytes = root.find(".//File_Size_K")
        if file_size_kilobytes is not None:
            pad_data["size_kilobytes"] = int(file_size_kilobytes.text.strip())

        # Дата релиза
        year = root.find(".//Program_Release_Year")
        month = root.find(".//Program_Release_Month")
        day = root.find(".//Program_Release_Day")
        if year is not None and month is not None and day is not None:
            pad_data["release_date"] = f"{year.text.strip()}-{month.text.strip().zfill(2)}-{day.text.strip().zfill(2)}"

        return pad_data

    except Exception as e:
        print(f"Ошибка при получении данных из {pad_url}: {e}")
        return None


def compare_pad_data(product_name, pad_data, expected_data):
    """Сравнивает фактические данные из PAD с ожидаемыми"""
    if not pad_data:
        pytest.fail(f"Не удалось получить данные PAD для {product_name}")

    # Сравнение названия
    expected_name = expected_data.get("name_in_pads", expected_data["name"])
    actual_name = pad_data.get("name", "")
    assert actual_name == expected_name, (
        f"Название не совпадает. Ожидалось: '{expected_name}', Получено: '{actual_name}'"
    )

    # Сравнение версии
    if "version" in expected_data:
        expected_version = str(expected_data["version"])
        actual_version = pad_data.get("version", "")
        assert actual_version == expected_version, (
            f"Версия не совпадает. Ожидалось: '{expected_version}', Получено: '{actual_version}'"
        )

    # Сравнение размера (MB)
    if "size" in expected_data:
        expected_size = str(expected_data["size"])
        actual_size = pad_data.get("size", "")
        assert actual_size == expected_size, (
            f"Размер (MB) не совпадает. Ожидалось: '{expected_size}', Получено: '{actual_size}'"
        )

    # Сравнение размера в байтах
    if "size_bytes" in expected_data:
        expected_bytes = int(expected_data["size_bytes"])
        actual_bytes = pad_data.get("size_bytes")
        assert actual_bytes == expected_bytes, (
            f"Размер в байтах не совпадает. Ожидалось: {expected_bytes}, Получено: {actual_bytes}"
        )

    # Сравнение размера в килобайтах
    if "size_kilobytes" in expected_data:
        expected_kb = int(expected_data["size_kilobytes"])
        actual_kb = pad_data.get("size_kilobytes")
        assert actual_kb == expected_kb, (
            f"Размер в КБ не совпадает. Ожидалось: {expected_kb}, Получено: {actual_kb}"
        )

    # Сравнение даты релиза
    if "release_date" in expected_data:
        expected_date = str(expected_data["release_date"])
        actual_date = pad_data.get("release_date", "")
        assert actual_date == expected_date, (
            f"Дата релиза не совпадает. Ожидалось: '{expected_date}', Получено: '{actual_date}'"
        )

    print(f"✅ Все данные для '{product_name}' ({expected_data['name']}) на языке '{list(PAD_FILE_MAPPING.keys()).index(product_name)+1}' совпадают.")


# === ГЕНЕРАЦИЯ ТЕСТОВ ДЛЯ КАЖДОЙ КОМБИНАЦИИ ПРОДУКТА И ЯЗЫКА ===
def pytest_generate_tests(metafunc):
    """Генерация параметров для тестов: один тест на продукт + язык"""
    if metafunc.function.__name__ == "test_pad_individual":
        cases = []
        ids = []
        for product_name in PAD_FILE_MAPPING:
            for lang in PAD_LANGUAGES:
                cases.append((product_name, lang))
                ids.append(f"{product_name}__{lang}")  # например: avs_video_remaker__en
        metafunc.parametrize("product_name,language", cases, ids=ids)


# === ОСНОВНОЙ ТЕСТ ===
def test_pad_individual(product_name, language, base_url):
    """
    Индивидуальный тест для проверки PAD-файла конкретного продукта на заданном языке.
    Имя теста формируется автоматически через pytest_generate_tests.
    """
    try:
        # Загружаем ожидаемые данные
        expected_data = load_editor_data(product_name)

        # Формируем URL PAD-файла
        pad_filename = PAD_FILE_MAPPING[product_name]
        pad_url = f"{base_url}/pads/{language}/{pad_filename}.xml"

        # Получаем данные из PAD
        pad_data = get_pad_data(pad_url)
        if pad_data is None:
            pytest.fail(f"❌ Не удалось получить данные из PAD-файла: {pad_url}")

        # Сравниваем
        compare_pad_data(product_name, pad_data, expected_data)

    except Exception as e:
        pytest.fail(f"❌ Ошибка при тестировании {product_name} ({language}): {e}")