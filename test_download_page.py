import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

url_end = "downloads.aspx"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def load_editor_data(product_name):
    with open("data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["products"][product_name]

def doTest(xpath, product_name, test_value, base_url, driver):
    full_url = f"{base_url}/{url_end}"
    driver.get(full_url)
    element = driver.find_element(By.XPATH, xpath)
    full_text = element.text.strip()
    actual_value = full_text.split(":")[1].strip()
    editor_data = load_editor_data(product_name)
    expected_value = editor_data[test_value]
    if actual_value == expected_value:
        print(f"Значение на странице: {actual_value} равно ожидаемому: {expected_value}")
    else:
        print(f"Значение на странице: {actual_value} не равно ожидаемому: {expected_value}")
    assert actual_value == expected_value, f"Ожидалось '{expected_value}', получено '{actual_value}'"


def test_VRm(driver, base_url):
    doTest("//h5[text()='AVS Video Remaker']/following-sibling::div[@class='tech-params']/p[1]", "avs_video_remaker", "version", base_url, driver)
    doTest("//h5[text()='AVS Video Remaker']/following-sibling::div[@class='tech-params']/p[2]", "avs_video_remaker", "release_date", base_url, driver)
    doTest("//h5[text()='AVS Video Remaker']/following-sibling::div[@class='tech-params']/p[3]", "avs_video_remaker", "size", base_url, driver)


def test_VE(driver, base_url):
    doTest("//h5[text()='AVS Video Editor']/following-sibling::div[@class='tech-params']/p[1]", "avs_video_editor", "version", base_url, driver)
    doTest("//h5[text()='AVS Video Editor']/following-sibling::div[@class='tech-params']/p[2]", "avs_video_editor", "release_date", base_url, driver)
    doTest("//h5[text()='AVS Video Editor']/following-sibling::div[@class='tech-params']/p[3]", "avs_video_editor", "size", base_url, driver)

def test_VC(driver, base_url):
    doTest("//h5[text()='AVS Video Converter']/following-sibling::div[@class='tech-params']/p[1]", "avs_video_converter", "version", base_url, driver)
    doTest("//h5[text()='AVS Video Converter']/following-sibling::div[@class='tech-params']/p[2]", "avs_video_converter", "release_date", base_url, driver)
    doTest("//h5[text()='AVS Video Converter']/following-sibling::div[@class='tech-params']/p[3]", "avs_video_converter", "size", base_url, driver)

def test_VP(driver, base_url):
    doTest("//h5[text()='AVS Media Player']/following-sibling::div[@class='tech-params']/p[1]", "avs_media_player", "version", base_url, driver)
    doTest("//h5[text()='AVS Media Player']/following-sibling::div[@class='tech-params']/p[2]", "avs_media_player", "release_date", base_url, driver)
    doTest("//h5[text()='AVS Media Player']/following-sibling::div[@class='tech-params']/p[3]", "avs_media_player", "size", base_url, driver)

def test_VD(driver, base_url):
    doTest("//h5[text()='AVS Audio Editor']/following-sibling::div[@class='tech-params']/p[1]", "avs_audio_editor", "version", base_url, driver)
    doTest("//h5[text()='AVS Audio Editor']/following-sibling::div[@class='tech-params']/p[2]", "avs_audio_editor", "release_date", base_url, driver)
    doTest("//h5[text()='AVS Audio Editor']/following-sibling::div[@class='tech-params']/p[3]", "avs_audio_editor", "size", base_url, driver)

def test_VR(driver, base_url):
    doTest("//h5[text()='AVS Audio Converter']/following-sibling::div[@class='tech-params']/p[1]", "avs_audio_converter", "version", base_url, driver)
    doTest("//h5[text()='AVS Audio Converter']/following-sibling::div[@class='tech-params']/p[2]", "avs_audio_converter", "release_date", base_url, driver)
    doTest("//h5[text()='AVS Audio Converter']/following-sibling::div[@class='tech-params']/p[3]", "avs_audio_converter", "size", base_url, driver)