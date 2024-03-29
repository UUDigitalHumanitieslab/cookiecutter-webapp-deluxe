import os
import pytest
from selenium import webdriver

WEBDRIVER_INI_NAME = 'webdriver'
BASE_ADDRESS_OPTION_NAME = 'base_address'


def pytest_addoption(parser):
    """ py.test hook where we register configuration options and defaults. """
    parser.addini(
        WEBDRIVER_INI_NAME,
        'Specify browsers in which the tests should run',
        type='linelist',
        default=['Chrome' ,'Firefox'],
    )
    parser.addoption(
        '--base-address',
        default='http://localhost:{{cookiecutter.backend_port}}/',
        help='specifies the base address where the application is running',
        dest=BASE_ADDRESS_OPTION_NAME,
    )


def pytest_generate_tests(metafunc):
    """ py.test hook where we inject configurable fixtures. """
    if 'webdriver_name' in metafunc.fixturenames:
        names = metafunc.config.getini(WEBDRIVER_INI_NAME)
        metafunc.parametrize('webdriver_name', names, scope='session')


@pytest.fixture(scope='session')
def webdriver_instance(webdriver_name):
    """ Provides a WebDriver instance that persists throughout the session.

        Use the `browser` fixture instead; it performs cleanups after each test.
    """
    if webdriver_name == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        driver = webdriver.Chrome(options=options)
    elif webdriver_name == 'Firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
    else:
        factory = getattr(webdriver, webdriver_name)
        driver = factory()
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def browser(webdriver_instance):
    """ Provides a WebDriver instance and performs some cleanups afterwards. """
    yield webdriver_instance
    webdriver_instance.delete_all_cookies()


@pytest.fixture(scope='session')
def base_address(pytestconfig):
    return pytestconfig.getoption(BASE_ADDRESS_OPTION_NAME)


@pytest.fixture
def api_address(base_address):
    return base_address + 'api/'


@pytest.fixture
def api_auth_address(base_address):
    return base_address + 'api-auth/'


@pytest.fixture
def admin_address(base_address):
    return base_address + 'admin/'
