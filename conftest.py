# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--site",
        action="store",
        default="production",
        help="Выбор сайта для тестирования: production, teststatic"
    )