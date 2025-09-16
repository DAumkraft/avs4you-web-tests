import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

url_end = "avs-video-editor.aspx"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # уберите, если нужен видимый браузер
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_video_display_and_functionality(driver, base_url):
    """Комплексный тест для проверки видео на странице"""

    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)

    # Проверяем наличие и видимость видео-элемента
    video_elements = driver.find_elements(By.TAG_NAME, "video")
    assert len(video_elements) > 0, "There should be at least one video element on the page"
    video_locator = video_elements[0]
    assert video_locator.is_displayed(), "Video element should be visible"

    # Проверяем атрибуты
    autoplay = video_locator.get_attribute("autoplay")
    loop = video_locator.get_attribute("loop")
    assert autoplay is not None and autoplay.lower() == "true", "Autoplay should be enabled"
    assert loop is not None and loop.lower() == "true", "Loop should be enabled"

    # Проверяем source элемент
    source_locator = video_locator.find_element(By.TAG_NAME, "source")
    assert source_locator is not None, "Source element should be present"

    # Проверяем стили (опционально)
    style = video_locator.get_attribute("style") or ""
    assert "position: absolute" in style, "Video should have absolute positioning"


def test_video_element_exists(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    video_locator = driver.find_element(By.TAG_NAME, "video")
    assert video_locator.is_displayed(), "Тэг video должен быть видимым"

def test_video_autoplay_and_loop_attributes(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    video = driver.find_element(By.TAG_NAME, "video")
    assert video.get_attribute("autoplay") is not None, "Проверка наличия атрибута autoplay"
    assert video.get_attribute("loop") is not None, "Проверка наличия атрибута loop"

def test_video_source_format(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    video = driver.find_element(By.TAG_NAME, "video")
    source = video.find_element(By.TAG_NAME, "source")
    src = source.get_attribute("src")
    assert src.endswith(".mp4"), "Проверка, что источник видео - файл .mp4"
    responce = requests.get(src, timeout=1)
    assert responce.status_code == 200, "Проверка доступности видео по ссылке"

def test_video_is_playable(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    video = driver.find_element(By.TAG_NAME, "video")
    # Проверяем, что видео не заблокировано и может быть воспроизведено
    assert video.is_enabled(), "Проверка, что видео доступно для воспроизведения"