import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

url_end = "register.aspx"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    # options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def load_editor_data():
    with open("data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["prices"]

list_of_langs = load_editor_data()

@pytest.mark.parametrize("lang", list_of_langs)
def test_check_price(lang, driver, base_url):
    if lang == "en":
        full_url = f"{base_url}/{url_end}"
    else:
        full_url = f"{base_url}/{lang}/{url_end}"
    print (full_url)
    driver.get(full_url)
    # tests for 1 year subscription
    actual_value = driver.find_element(By.CSS_SELECTOR,".buy-block:not(.unlimited-block) [font-weight='500'].current-price-text")  
    price_1year_onsite = actual_value.text
    prices_from_yaml = list_of_langs[lang]
    price_1year_yaml = prices_from_yaml["oneyear"]
    assert price_1year_onsite == price_1year_yaml
    # Test for unlimited subscription
    actual_value = driver.find_element(By.CSS_SELECTOR,".buy-block.unlimited-block .current-price-text")  
    price_unlimited_onsite = actual_value.text
    prices_from_yaml = list_of_langs[lang]
    price_unlimited_yaml = prices_from_yaml["unlimited"]
    assert price_unlimited_onsite == price_unlimited_yaml
    