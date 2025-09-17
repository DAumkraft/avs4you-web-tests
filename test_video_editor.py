import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

url_end = "avs-video-editor.aspx"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def load_editor_data():
    with open("data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["products"]["avs_video_editor"]

def test_version(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    element = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div[3]/main/div/div[9]/div[1]/div[2]/p[2]')
    actual_value = element.text.strip()

    editor_data = load_editor_data()
    expected_value = editor_data["version"]

    if actual_value == expected_value:
        print(f"Значение на странице: {actual_value} равно ожидаемому: {expected_value}")
    else:
        print(f"Значение на странице: {actual_value} не равно ожидаемому: {expected_value}")
        
    assert actual_value == expected_value, f"Ожидалось '{expected_value}', получено '{actual_value}'"

def test_short_version(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    element = driver.find_element(By.XPATH, '//*[@id="screenshotsCarousel"]')
    actual_value = element.text.strip()

    editor_data = load_editor_data()
    expected_value = str(editor_data["short_version"])

    if actual_value == expected_value:
        print(f"Значение на странице: {actual_value} равно ожидаемому: {expected_value}")
    else:
        print(f"Значение на странице: {actual_value} не равно ожидаемому: {expected_value}")
        
    assert actual_value == expected_value, f"Ожидалось '{expected_value}', получено '{actual_value}'"

def test_size(driver, base_url):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    element = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div[3]/main/div/div[9]/div[1]/div[1]/p[2]')
    actual_value = element.text.strip()

    editor_data = load_editor_data()
    expected_value = editor_data["size"]

    if actual_value == expected_value:
        print(f"Размер элемента: {actual_value} соответствует ожидаемому: {expected_value}")
    else:
        print(f"Размер элемента: {actual_value} не соответствует ожидаемому: {expected_value}")

    assert actual_value == expected_value, f"Ожидалось '{expected_value}', получено '{actual_value}'"