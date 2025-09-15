import pytest

URLS = {
    "production": "https://avs4you.com",
    "teststatic": "https://teststatic.avs4you.com"
}

def pytest_addoption(parser):
    parser.addoption(
        "--site",
        action="store",
        default="production",
        help="Выбор сайта для тестирования: production, teststatic"
    )

@pytest.fixture
def base_url(request):
    site_name = request.config.getoption("--site")
    return URLS.get(site_name, URLS["production"])